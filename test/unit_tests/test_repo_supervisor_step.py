__author__ = 'tinglev'

import unittest
from unittest.mock import MagicMock
import os
import json
from modules.pipeline_steps.repo_supervisor_step import RepoSupervisorStep
from modules.util import environment

class RepoSupervisorStepTest(unittest.TestCase):

    def get_test_data_project_root(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '../data')

    def test_all_patterns_are_include(self):
        step = RepoSupervisorStep()
        number_of_patterns = 4
        os.environ[environment.PROJECT_ROOT] = self.get_test_data_project_root()
        self.assertEqual(number_of_patterns, len(step.get_ignore_patterns()))

    def test_get_default_output_file(self):
        step = RepoSupervisorStep()
        os.environ[environment.PROJECT_ROOT] = self.get_test_data_project_root()
        #/tmp/myfile.js
        #/node_modules/
        #/secrets
        # + RepoSupervisor.EXCLUDED_DIRECTORIES
        self.assertTrue(step.ignore(RepoSupervisorStep.REPO_MOUNTED_DIR + '/tmp/myfile.js'))
        self.assertFalse(step.ignore(RepoSupervisorStep.REPO_MOUNTED_DIR + '/tmp/myfile'))
        self.assertTrue(step.ignore(RepoSupervisorStep.REPO_MOUNTED_DIR + '/node_modules/')) # From EXCLUDED_DIRECTORIES
        self.assertTrue(step.ignore(RepoSupervisorStep.REPO_MOUNTED_DIR + '/packages/'))

    def test_excluded_directories_are_ignored(self):
        step = RepoSupervisorStep()
        os.environ[environment.PROJECT_ROOT] = self.get_test_data_project_root()
        self.assertTrue(step.ignore(RepoSupervisorStep.REPO_MOUNTED_DIR + '/node_modules/')) # From EXCLUDED_DIRECTORIES

    def test_process_supervisor_result(self):
        RepoSupervisorStep.REPO_MOUNTED_DIR = './test/fixtures/integration/dir.with.secrets'
        step = RepoSupervisorStep()
        step._log_warning_and_send_to_slack = MagicMock()
        output_path = os.path.join(self.get_test_data_project_root(), 'supervisor/output.json')
        with open(output_path, 'r') as output_file:
            output = output_file.read()
        filenames = step._process_supervisor_result(output, None)
        self.assertEqual(filenames, [b'/foo/bar.js', b'/foo/foo.json'])
