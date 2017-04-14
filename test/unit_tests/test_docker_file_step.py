__author__ = 'tinglev'

import os
import unittest
from mock import patch
from modules.util.environment import Environment
from modules.pipeline_steps.docker_file_step import DockerFileStep

class DockerFileTests(unittest.TestCase):

    def test_docker_file_exists(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        dfs = DockerFileStep()
        result = dfs.docker_file_exists()
        self.assertTrue(result)
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data/')
        result = dfs.docker_file_exists()
        self.assertTrue(result)
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data//')
        result = dfs.docker_file_exists()
        self.assertTrue(result)
