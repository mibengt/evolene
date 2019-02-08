__author__ = 'tinglev'

import unittest
from unittest import mock
from modules.pipeline_steps.npm_version_changed_step import NpmVersionChangedStep
from modules.util.data import Data

class NpmVersionChangedStepTests(unittest.TestCase):

    def test_run_step(self):
        data = {Data.NPM_PACKAGE_NAME: 'kth-azure-app', Data.NPM_PACKAGE_VERSION: '1.0.0'}
        version_step = NpmVersionChangedStep()
        NpmVersionChangedStep.get_latest_version = mock.MagicMock()
        NpmVersionChangedStep.get_latest_version.return_value = '1.0.0'
        result = version_step.run_step(data)
        self.assertFalse(result[Data.NPM_VERSION_CHANGED])
        NpmVersionChangedStep.get_latest_version.return_value = '15.0.15'
        result = version_step.run_step(data)
        self.assertTrue(result[Data.NPM_VERSION_CHANGED])
        NpmVersionChangedStep.get_latest_version.return_value = '0.0.15'
        result = version_step.run_step(data)
        self.assertTrue(result[Data.NPM_VERSION_CHANGED])
        NpmVersionChangedStep.get_latest_version.return_value = '0.10.0'
        result = version_step.run_step(data)
        self.assertTrue(result[Data.NPM_VERSION_CHANGED])
