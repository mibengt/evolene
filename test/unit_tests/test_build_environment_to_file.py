__author__ = 'tinglev'

import unittest
import os
from modules.pipeline_steps.build_environment_to_file_step import BuildEnvironmentToFileStep
from modules.util import environment
from modules.util import pipeline_data


class BuildEnvironmentToFileStepTest(unittest.TestCase):

    def test_get_default_output_file(self):
        step = BuildEnvironmentToFileStep()
        os.environ[environment.PROJECT_ROOT] = "/tmp"
        self.assertNotEqual("/tmp", step.get_ouput_file)

    def test_output_file_is_relative(self):
        step = BuildEnvironmentToFileStep()
        os.environ[environment.PROJECT_ROOT] = "/tmp"
        os.environ[environment.BUILD_INFORMATION_OUTPUT_FILE] = "/path/file.json"
        self.assertEqual("/path/file.json", step.get_ouput_file())

    def test_output_file_is_none(self):
        step = BuildEnvironmentToFileStep()
        os.environ[environment.PROJECT_ROOT] = "/tmp"
        self.assertIsNone(step.get_ouput_file())

    def test_output(self):
        os.environ[environment.BUILD_NUMBER] = "1"
        os.environ[environment.GIT_BRANCH] = "master"
        os.environ[environment.GIT_COMMIT] = "12345a"
        data = {
            pipeline_data.IMAGE_NAME: "test-app",
            pipeline_data.IMAGE_VERSION: "test-app:1.1.3_12345a"
        }
        step = BuildEnvironmentToFileStep()
        output = step.get_build_environment(data)
        self.assertEqual(output["gitBranch"], "master")
        self.assertEqual(output["gitCommit"], "12345a")
        self.assertEqual(output["jenkinsBuild"], "1")
        self.assertEqual(output["dockerName"], "test-app")
        self.assertEqual(output["dockerVersion"], "test-app:1.1.3_12345a")
