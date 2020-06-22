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

    def test_get_latest_version_for_major_minor(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
                pipeline_data.NPM_PACKAGE_VERSION: '0.0.6'
        }

        NpmVersionChangedStep.get_versions_for_major_minor = mock.MagicMock()   
        NpmVersionChangedStep.get_versions_for_major_minor.return_value = [
            "0.0.1",
            "0.0.2",
            "0.0.3",
            "0.0.4",
            "0.0.5",
            "0.0.6",
            "0.0.7",
            "0.0.8"
        ]

        self.assertEqual(NpmVersionChangedStep.get_latest_version_for_major_minor(version_step, data), "0.0.8")

    def test_get_latest_version_for_major_minor_is_none_when_no_previous_exits(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
                pipeline_data.NPM_PACKAGE_VERSION: '2.0.0'
        }

        NpmVersionChangedStep.get_versions_for_major_minor = mock.MagicMock()   
        NpmVersionChangedStep.get_versions_for_major_minor.return_value = []

        self.assertIsNone(version_step.get_latest_version_for_major_minor(data))


    def test_version_is_already_published(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
                pipeline_data.NPM_PACKAGE_VERSION: '0.1.6'
        }

        version_step.check_npm_for_version = mock.MagicMock()   
        version_step.check_npm_for_version.return_value = "0.1.6"

        published = version_step.is_version_already_published(data)
        
        self.assertTrue(published)

    # def test_version_is_not_already_published(self):

    #     version_step = NpmVersionChangedStep()

    #     data = {
    #             pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
    #             pipeline_data.NPM_PACKAGE_VERSION: '0.0.1337'
    #     }

    #     version_step.check_npm_for_version = mock.MagicMock()   
    #     version_step.check_npm_for_version.return_value = None
        
    #     published = version_step.is_version_already_published(data)
        
    #     self.assertFalse(published)


    def test_get_major_minor_from_packagejson(self):

        version_step = NpmVersionChangedStep()

        self.assertEqual(version_step.get_major_minor({
                pipeline_data.NPM_PACKAGE_VERSION: '2.3.4'
        }), "2.3")
        
        self.assertEqual(version_step.get_major_minor({
                pipeline_data.NPM_PACKAGE_VERSION: '3.4.4'
        }), "3.4")
