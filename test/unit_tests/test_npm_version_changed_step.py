__author__ = 'tinglev'

import unittest
from unittest import mock
from modules.pipeline_steps.npm_version_changed_step import NpmVersionChangedStep
from modules.util import pipeline_data


class NpmVersionChangedStepTests(unittest.TestCase):

    def test_run_step(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: 'kth-azure-app',
                pipeline_data.NPM_PACKAGE_VERSION: '1.0.0'
        }

        NpmVersionChangedStep.get_latest_version = mock.MagicMock()      
        NpmVersionChangedStep.get_latest_version_for_major_minor = mock.MagicMock()                
        NpmVersionChangedStep.is_version_already_published = mock.MagicMock()                

        NpmVersionChangedStep.get_latest_version.return_value = '1.0.0'
        NpmVersionChangedStep.get_latest_version_for_major_minor.return_value = '1.0'

        result = version_step.run_step(data)
        self.assertFalse(result[pipeline_data.NPM_VERSION_CHANGED])

        NpmVersionChangedStep.get_latest_version.return_value = '15.0.15'
        result = version_step.run_step(data)
        self.assertTrue(result[pipeline_data.NPM_VERSION_CHANGED])

        NpmVersionChangedStep.get_latest_version.return_value = '0.0.15'
        result = version_step.run_step(data)
        self.assertTrue(result[pipeline_data.NPM_VERSION_CHANGED])

        NpmVersionChangedStep.get_latest_version.return_value = '0.10.0'
        result = version_step.run_step(data)
        self.assertTrue(result[pipeline_data.NPM_VERSION_CHANGED])


    def test_get_major_minor_from_packagejson(self):

        version_step = NpmVersionChangedStep()

        self.assertEqual(version_step.get_major_minor({
                pipeline_data.NPM_PACKAGE_VERSION: '2.3.4'
        }), "2.3")
        
        self.assertEqual(version_step.get_major_minor({
                pipeline_data.NPM_PACKAGE_VERSION: '3.4.4'
        }), "3.4")
