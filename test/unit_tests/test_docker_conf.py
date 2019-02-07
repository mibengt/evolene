__author__ = 'tinglev'

import unittest
import os
from modules.util.environment import Environment
from modules.util.data import Data
from modules.pipeline_steps.read_conf_step import ReadConfFileStep
from modules.util.file_util import FileUtil

class DockerConfStepTests(unittest.TestCase):

    def get_test_data_project_root(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../data')

    def test_clean_variable_value(self):
        dcs = ReadConfFileStep('docker.conf', [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        result = dcs.clean_variable_value('""bla""')
        self.assertEqual(result, 'bla')
        result = dcs.clean_variable_value('b"l"a')
        self.assertEqual(result, 'b"l"a')
        result = dcs.clean_variable_value('"b\\"l\\"a"')
        self.assertEqual(result, 'b\\"l\\"a')

    def test_trim(self):
        dcs = ReadConfFileStep('docker.conf', [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = []
        result = dcs.trim(lines)
        self.assertEqual(result, [])
        lines = ['#comment']
        result = dcs.trim(lines)
        self.assertEqual(result, [])
        lines = ['#comment', 'ENV=TEST']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'radomtext']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'BAD_ENV=']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', '=BAD_ENV']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'ENV_2=TEST 2']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=TEST'])
        lines = ['#comment', 'ENV=TEST', 'ENV_2="TEST 2"']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=TEST', 'ENV_2="TEST 2"'])
        lines = ['#comment', 'ENV=1.0']
        result = dcs.trim(lines)
        self.assertEqual(result, ['ENV=1.0'])

    def test_add_conf_vars(self):
        dcs = ReadConfFileStep('docker.conf', [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        env_lines = None
        result = dcs.add_conf_vars(env_lines, {'data':'abc'})
        self.assertEqual(result, {'data':'abc'})
        env_lines = []
        result = dcs.add_conf_vars(env_lines, {'data':'abc'})
        self.assertEqual(result, {'data':'abc'})
        env_lines = ['test_key=test_val']
        result = dcs.add_conf_vars(env_lines, {})
        self.assertEqual(result['test_key'], 'test_val')
        env_lines = ['test_key=test_val', 'test_2_key=test_2_val']
        result = dcs.add_conf_vars(env_lines, {})
        self.assertEqual(result['test_key'], 'test_val')
        self.assertEqual(result['test_2_key'], 'test_2_val')

    def test_image_version_in_data(self):
        dcs = ReadConfFileStep('docker.conf', [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        env_lines = dcs.trim(['#comment', 'IMAGE_NAME=TEST',
                              'IMAGE_VERSION=1.3', 'PATCH_VERSION=0'])
        result = dcs.add_conf_vars(env_lines, {})
        self.assertEqual(result[Data.PATCH_VERSION], '0')

    def test_get_docker_conf_lines(self):
        os.environ[Environment.PROJECT_ROOT] = self.get_test_data_project_root()
        ReadConfFileStep('docker.conf', [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        result = FileUtil.get_lines("/docker.conf")
        self.assertEqual(len(result), 13)
        self.assertEqual(result[12], 'ADDITIONAL_ENV="Some value"')

    def test_missing_conf_vars(self):
        dcs = ReadConfFileStep('docker.conf', [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = None
        result = dcs.get_missing_conf_vars(lines)
        self.assertEqual(result, [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = []
        result = dcs.get_missing_conf_vars(lines)
        self.assertEqual(result, [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = ['{}=test'.format(Environment.IMAGE_NAME)]
        result = dcs.get_missing_conf_vars(lines)
        self.assertEqual(result, [Data.IMAGE_VERSION])
        lines = ['{}=test'.format(Environment.IMAGE_NAME),
                 '{}=test'.format(Data.IMAGE_VERSION)]
        result = dcs.get_missing_conf_vars(lines)
        self.assertEqual(result, [])
        lines = ['bla=test', 'lba2=test']
        result = dcs.get_missing_conf_vars(lines)
        self.assertEqual(result, [Environment.IMAGE_NAME, Data.IMAGE_VERSION])
        lines = ['{}=kopps'.format(Environment.IMAGE_NAME),
                 '{}=1.0'.format(Data.IMAGE_VERSION)]
        result = dcs.get_missing_conf_vars(lines)
        self.assertEqual(result, [])
