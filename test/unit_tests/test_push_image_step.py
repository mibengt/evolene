__author__ = 'tinglev'

import os
import unittest
from mock import patch
from modules.pipeline_steps.push_image_step import PushImageStep
from modules.util.data import Data
from modules.util.exceptions import PipelineException
from modules.util.environment import Environment

class PushImageStepTests(unittest.TestCase):

    def test_verify_image_in_tags(self):
        pis = PushImageStep()
        data = {Data.IMAGE_VERSION: '1.1.23_2135'}
        result = pis.verify_image_version_in_tags(['1.1.23_2135', '1.2.0_1234'], data)
        self.assertTrue(result)
        self.assertRaises(PipelineException,
                          pis.verify_image_version_in_tags, ['1.1.23_2136', '1.2.0_1234'], data)

    def test_get_image_to_push(self):
        pis = PushImageStep()
        os.environ[Environment.REGISTRY_HOST] = 'https://kthregistryv2.sys.kth.se'
        data = {'LOCAL_IMAGE_ID': 'kth-azure-app:1.2.0_1234'}
        result = pis.get_image_to_push(data)
        self.assertEqual(result, 'kthregistryv2.sys.kth.se/kth-azure-app:1.2.0_1234')

    def test_create_registry_url(self):
        pis = PushImageStep()
        os.environ[Environment.REGISTRY_HOST] = 'kthregistryv2.sys.kth.se'
        os.environ[Environment.IMAGE_NAME] = 'kth-azure-app'
        result = pis.create_registry_url()
        self.assertEqual(result, 'https://kthregistryv2.sys.kth.se/v2/kth-azure-app/tags/list')
