__author__ = 'tinglev'

import os
import unittest
from modules.util import environment
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.util import pipeline_data

class DockerFileTests(unittest.TestCase):

    def get_test_data_project_root(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../data')

    def test_dockerfile_set(self):
        step = DockerFileStep()
        os.environ[environment.PROJECT_ROOT] = self.get_test_data_project_root()
        data = step.run_step({})
        self.assertTrue(str(data[pipeline_data.DOCKERFILE_FILE]).endswith(DockerFileStep.FILE_DOCKERFILE))
