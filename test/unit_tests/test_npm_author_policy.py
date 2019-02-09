__author__ = 'tinglev'

import os
import unittest
import sys
from unittest import mock
from modules.pipeline_steps.npm_author_policy import NpmAuthorPolicy
from modules.pipeline_steps.load_package_json_step import LoadPackageJsonStep
from modules.util import environment, pipeline_data

class NpmVersionStepTests(unittest.TestCase):

    def test_run_step(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[environment.PROJECT_ROOT] = os.path.join(current_path, '../data/npm')
        load_step = LoadPackageJsonStep()
        data = load_step.run_step({})
        sys.exit = mock.MagicMock()
        step = NpmAuthorPolicy()
        step.run_step(data)
        sys.exit.assert_called_once()
        data[pipeline_data.PACKAGE_JSON]['author'] = {
            'name': 'Test'
        }
        sys.exit.reset_mock()
        step.run_step(data)
        sys.exit.assert_called_once()
        data[pipeline_data.PACKAGE_JSON]['author'] = {
            'email': 'test@kth.se'
        }
        sys.exit.reset_mock()
        step.run_step(data)
        sys.exit.assert_called_once()
        data[pipeline_data.PACKAGE_JSON]['author'] = {
            'email': 'test@kth.se',
            'name': 'Test'
        }
        sys.exit.reset_mock()
        step.run_step(data)
        sys.exit.assert_not_called()
