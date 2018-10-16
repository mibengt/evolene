__author__ = 'tinglev'

import unittest
import os
from modules.util.environment import Environment
from modules.util.file_util import FileUtil

class FileUtilTests(unittest.TestCase):

    def get_test_data_project_root(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../data')

    def test_get_content_as_array(self):
        rows_in_file = 3
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        self.assertEqual(rows_in_file, len(FileUtil.get_rows_as_array('.scanignore')))

    def test_is_directory(self):
        os.environ[Environment.PROJECT_ROOT] = self.get_test_data_project_root()
        self.assertTrue(FileUtil.is_directory('/'))

    def test_is_file(self):
        os.environ[Environment.PROJECT_ROOT] = self.get_test_data_project_root()
        self.assertFalse(FileUtil.is_directory('/docker.conf'))
