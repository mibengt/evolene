__author__ = 'tinglev'

import unittest
from unittest import mock
from modules.pipeline_steps.npm_version_changed_step import NpmVersionChangedStep
from modules.util import pipeline_data, file_util

class NpmVersionChangedStepTests(unittest.TestCase):

    def test_run_step(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: 'kth-azure-app',
                pipeline_data.NPM_PACKAGE_VERSION: '1.0.0'
        }

        NpmVersionChangedStep.version_exists = mock.MagicMock()      
        NpmVersionChangedStep.get_latest_version = mock.MagicMock()                
        NpmVersionChangedStep.version_exists = mock.MagicMock()                

        NpmVersionChangedStep.version_exists.return_value = True
        NpmVersionChangedStep.get_latest_version.return_value = '1.0.0'

        result = version_step.run_step(data)
        self.assertFalse(result[pipeline_data.NPM_VERSION_CHANGED])

        NpmVersionChangedStep.version_exists.return_value = False
        result = version_step.run_step(data)
        self.assertTrue(result[pipeline_data.NPM_VERSION_CHANGED])


    def test_get_latest_version(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
                pipeline_data.NPM_PACKAGE_VERSION: '0.0.6'
        }

        version_step.get_versions = mock.MagicMock()   
        version_step.get_versions.return_value = [
            "0.0.1",
            "0.0.2",
            "0.0.3",
            "0.0.4",
            "0.0.5",
            "0.0.6",
            "0.0.7",
            "0.0.8"
        ]

        self.assertEqual(version_step.get_latest_version(data), "0.0.8")

    def test_get_latest_version_is_none_when_no_previous_exits(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
                pipeline_data.NPM_PACKAGE_VERSION: '2.0.0'
        }

        NpmVersionChangedStep.get_versions = mock.MagicMock()   
        NpmVersionChangedStep.get_versions.return_value = []

        self.assertIsNone(version_step.get_latest_version(data))

    def test_version_exists(self):

        version_step = NpmVersionChangedStep()

        data = {
                pipeline_data.NPM_PACKAGE_NAME: '@kth/npm-template',
                pipeline_data.NPM_PACKAGE_VERSION: '2.0.0'
        }

        version_step.get_version = mock.MagicMock()   
        version_step.get_version.return_value = "2.0.0"
#        self.assertEqual(version_step.version_exists(data), True)

        version_step.get_version = mock.MagicMock()
        version_step.get_version.return_value = None
        self.assertEqual(version_step.version_exists(data), False)


    # def test_get_major_minor_from_packagejson(self):

    #     version_step = NpmVersionChangedStep()

    #     self.assertEqual(version_step.get_major_minor({
    #             pipeline_data.NPM_PACKAGE_VERSION: '2.3.4'
    #     }), "2.3")
        
    #     self.assertEqual(version_step.get_major_minor({
    #             pipeline_data.NPM_PACKAGE_VERSION: '3.4.4'
    #     }), "3.4")

    

    # def test_get_latest_patch_version(self):
    #     data = {pipeline_data.NPM_MAJOR_MINOR_LATEST: '1.2.3'}
    #     version_step = NpmVersionChangedStep()
    #     self.assertEquals(version_step.get_latest_patch_version(data), 3)

    #     data = {pipeline_data.NPM_MAJOR_MINOR_LATEST: '1.2.455'}
    #     version_step = NpmVersionChangedStep()
    #     self.assertEquals(version_step.get_latest_patch_version(data), 455)

    # def test_get_major_minor_version(self):
    #     data = {pipeline_data.NPM_PACKAGE_VERSION: '1.2.3'}
    #     version_step = NpmVersionChangedStep()
    #     self.assertEquals(version_step.get_major_minor(data), "1.2")

    #     data = {pipeline_data.NPM_PACKAGE_VERSION: '34.56.455'}
    #     version_step = NpmVersionChangedStep()
    #     self.assertEquals(version_step.get_major_minor(data), "34.56")

    # def test_get_next_patch_version(self):
    #     data = {pipeline_data.NPM_MAJOR_MINOR_LATEST: '1.2.35'}
    #     version_step = NpmVersionChangedStep()
    #     self.assertEquals(version_step.get_next_patch_version(data), 36)

    # def test_get_new_version(self):
    #     data = {pipeline_data.NPM_MAJOR_MINOR_LATEST: '3.2.35', pipeline_data.NPM_PACKAGE_VERSION: '3.2.0' }
    #     version_step = NpmVersionChangedStep()
    #     self.assertEquals(version_step.get_next_version(data), "3.2.36")

    # def test_update_version_ignore_patch_version_higher_then_on_npm(self):
    #     data = {
    #         pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4', 'automaticPublish': 'true'},
    #         pipeline_data.NPM_MAJOR_MINOR_LATEST: "2.3.0",
    #         pipeline_data.NPM_PACKAGE_VERSION: "2.3.4"
    #     }
    #     version_step = NpmVersionChangedStep()
    #     version_step.increase_version(data)
    #     self.assertEqual(data[pipeline_data.PACKAGE_JSON]["version"], "2.3.1")

    # def test_update_version_ignore_patch_version_lower_then_on_npm(self):
    #     data = {
    #         pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4', 'automaticPublish': 'true'},
    #         pipeline_data.NPM_PACKAGE_VERSION: "2.3.4",
    #         pipeline_data.NPM_MAJOR_MINOR_LATEST: "2.3.99"
    #     }
    #     version_step = NpmVersionChangedStep()
    #     version_step.increase_version(data)
    #     self.assertEqual(data[pipeline_data.PACKAGE_JSON]["version"], "2.3.100")

    # def test_automaticPublish(self):
    #     data = {pipeline_data.NPM_MAJOR_MINOR_LATEST: '3.2.35'}
    #     version_step = NpmVersionChangedStep()
    #     self.assertFalse(version_step.use_automatic_publish(data))

    #     data = {pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4' }}
    #     version_step = NpmVersionChangedStep()
    #     self.assertFalse(version_step.use_automatic_publish(data))

    #     data = {pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4', 'automaticPublish': 'true'}}
    #     version_step = NpmVersionChangedStep()
    #     self.assertTrue(version_step.use_automatic_publish(data))
