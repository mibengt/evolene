__author__ = 'tinglev'

import unittest
import os
from modules.pipeline_steps.build_environment_to_file_step import BuildEnvironmentToFileStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.exceptions import PipelineException

class BuildEnvironmentToFileStepTest(unittest.TestCase):

    def test_get_default_output_file(self):
        step = BuildEnvironmentToFileStep()
        os.environ[Environment.PROJECT_ROOT] = "/tmp"
        self.assertNotEqual("/tmp", step.get_ouput_file)

    def test_get_output_file(self):
        step = BuildEnvironmentToFileStep()
        os.environ[Environment.PROJECT_ROOT] = "/tmp"
        os.environ[Environment.BUILD_INFORMATION_OUTPUT_FILE] = "/path/file.json"
        self.assertEqual("/tmp/path/file.json", step.get_ouput_file())

    def test_output(self):
        
        os.environ[Environment.BUILD_NUMBER] = "1"
        os.environ[Environment.GIT_BRANCH] = "master"
        os.environ[Environment.GIT_COMMIT] = "12345a"

        data = {
            Data.IMAGE_NAME: "test-app",
            Data.IMAGE_VERSION: "test-app:1.1.3_12345a"
        }
        
        step = BuildEnvironmentToFileStep()

        output = step.get_build_environment(data)

        self.assertEqual(output["gitBranch"], "master")
        self.assertEqual(output["gitCommit"], "12345a")
        self.assertEqual(output["jenkinsBuild"], "1")
        self.assertEqual(output["dockerName"], "test-app")
        self.assertEqual(output["dockerVersion"], "test-app:1.1.3_12345a")