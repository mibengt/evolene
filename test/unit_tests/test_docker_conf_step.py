__author__ = 'tinglev'

import unittest
import os
from mock import patch
from modules.util.environment import Environment
from modules.util.data import Data
from modules.pipeline_steps.docker_conf_step import DockerConfPipelineStep

class DockerConfStepTests(unittest.TestCase):

    def test_clean_variable_value(self):
        dcs = DockerConfPipelineStep()
        result = dcs.clean_variable_value('""bla""')
        self.assertEqual(result, 'bla')
        result = dcs.clean_variable_value('b"l"a')
        self.assertEqual(result, 'b"l"a')
        result = dcs.clean_variable_value('"b\\"l\\"a"')
        self.assertEqual(result, 'b\\"l\\"a')

    def test_get_docker_conf_path(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        dcs = DockerConfPipelineStep()
        result = dcs.docker_conf_exists()
        self.assertTrue(result)
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data/')
        result = dcs.docker_conf_exists()
        self.assertTrue(result)
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data//')
        result = dcs.docker_conf_exists()
        self.assertTrue(result)
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../dat')
        result = dcs.docker_conf_exists()
        self.assertFalse(result)

    def test_get_docker_conf_env_lines(self):
        dcs = DockerConfPipelineStep()
        lines = []
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, [])
        lines = ['#comment']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, [])
        lines = ['#comment', 'ENV=TEST']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'radomtext']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'BAD_ENV=']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', '=BAD_ENV']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'ENV_2=TEST 2']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'ENV_2="TEST 2"']
        result = dcs.get_docker_conf_env_lines(lines)
        self.assertEqual(result, ['ENV=TEST', 'ENV_2="TEST 2"'])

    def test_add_env_lines_to_data(self):
        dcs = DockerConfPipelineStep()
        env_lines = None
        result = dcs.add_env_lines_to_data(env_lines, {'data':'abc'})
        self.assertEqual(result, {'data':'abc'})
        env_lines = []
        result = dcs.add_env_lines_to_data(env_lines, {'data':'abc'})
        self.assertEqual(result, {'data':'abc'})
        env_lines = ['test_key=test_val']
        result = dcs.add_env_lines_to_data(env_lines, {})
        self.assertEqual(result['test_key'], 'test_val')
        env_lines = ['test_key=test_val', 'test_2_key=test_2_val']
        result = dcs.add_env_lines_to_data(env_lines, {})
        self.assertEqual(result['test_key'], 'test_val')
        self.assertEqual(result['test_2_key'], 'test_2_val')

    def test_get_docker_conf_lines(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        dcs = DockerConfPipelineStep()
        result = dcs.get_docker_conf_lines()
        self.assertEqual(len(result), 13)
        self.assertEqual(result[12], 'ADDITIONAL_ENV="Some value"')

    def test_missing_conf_vars(self):
        dcs = DockerConfPipelineStep()
        lines = None
        result = dcs.missing_conf_vars(lines)
        self.assertEqual(result, [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = []
        result = dcs.missing_conf_vars(lines)
        self.assertEqual(result, [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = ['{}=test'.format(Environment.IMAGE_NAME)]
        result = dcs.missing_conf_vars(lines)
        self.assertEqual(result, [Data.IMAGE_VERSION])
        lines = ['{}=test'.format(Environment.IMAGE_NAME),
                 '{}=test'.format(Data.IMAGE_VERSION)]
        result = dcs.missing_conf_vars(lines)
        self.assertEqual(result, [])
        lines = ['bla=test', 'lba2=test']
        result = dcs.missing_conf_vars(lines)
        self.assertEqual(result, [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
