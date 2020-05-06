__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.npm_publish_step import NpmPublishStep
from modules.util import pipeline_data

class NpmPublishStepTests(unittest.TestCase):

    def test_get_latest_patch_version(self):
        data = {pipeline_data.NPM_LATEST_VERSION: '1.2.3'}
        version_step = NpmPublishStep()
        self.assertEquals(version_step.get_latest_patch_version(data), 3)

        data = {pipeline_data.NPM_LATEST_VERSION: '1.2.455'}
        version_step = NpmPublishStep()
        self.assertEquals(version_step.get_latest_patch_version(data), 455)

    def test_get_major_minor_version(self):
        data = {pipeline_data.NPM_LATEST_VERSION: '1.2.3'}
        version_step = NpmPublishStep()
        self.assertEquals(version_step.get_major_minor_version(data), "1.2")

        data = {pipeline_data.NPM_LATEST_VERSION: '34.56.455'}
        version_step = NpmPublishStep()
        self.assertEquals(version_step.get_major_minor_version(data), "34.56")

    def test_get_next_patch_version(self):
        data = {pipeline_data.NPM_LATEST_VERSION: '1.2.35'}
        version_step = NpmPublishStep()
        self.assertEquals(version_step.get_next_patch_version(data), 36)

    def test_get_new_version(self):
        data = {pipeline_data.NPM_LATEST_VERSION: '3.2.35'}
        version_step = NpmPublishStep()
        self.assertEquals(version_step.get_next_version(data), "3.2.36")

    def test_update_version_ignore_patch_version_higher_then_on_npm(self):
        data = {
            pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4', 'automaticPublish': 'true'},
            pipeline_data.NPM_LATEST_VERSION: "2.3.0"
        }
        version_step = NpmPublishStep()
        version_step.update_patch_version(data)
        self.assertEqual(data[pipeline_data.PACKAGE_JSON]["version"], "2.3.1")

    def test_update_version_ignore_patch_version_lower_then_on_npm(self):
        data = {
            pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4', 'automaticPublish': 'true'},
            pipeline_data.NPM_LATEST_VERSION: "2.3.99"
        }
        version_step = NpmPublishStep()
        version_step.update_patch_version(data)
        self.assertEqual(data[pipeline_data.PACKAGE_JSON]["version"], "2.3.100")

    def test_automaticPublish(self):
        data = {pipeline_data.NPM_LATEST_VERSION: '3.2.35'}
        version_step = NpmPublishStep()
        self.assertFalse(version_step.use_automatic_publish(data))

        data = {pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4' }}
        version_step = NpmPublishStep()
        self.assertFalse(version_step.use_automatic_publish(data))

        data = {pipeline_data.PACKAGE_JSON: {'name': 'my-package', 'version': '2.3.4', 'automaticPublish': 'true'}}
        version_step = NpmPublishStep()
        self.assertTrue(version_step.use_automatic_publish(data))