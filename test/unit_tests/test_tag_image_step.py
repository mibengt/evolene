__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.tag_image_step import TagImageStep
from modules.util.data import Data

class TagImageStepTests(unittest.TestCase):

    def test_format_tag(self):
        tis = TagImageStep()
        
        data = {
            Data.LOCAL_IMAGE_ID: '9871234192',
            Data.IMAGE_VERSION:'1.0.1_abcdef',
            Data.COMMIT_HASH:'fedcba',
            Data.IMAGE_NAME: 'kth-azure-app',
        }

        result = tis.get_default_tag(data, registry_host="host.com")
        self.assertEqual(result, 'host.com/kth-azure-app:1.0.1_abcdef')

    def test_format_tag_not_using_hash_key(self):
        tis = TagImageStep()
        
        data = {
            Data.LOCAL_IMAGE_ID: '9871234192',
            Data.IMAGE_VERSION:'1.0.3',
            Data.SEM_VER:'1.0.3',
            Data.COMMIT_HASH:'abcdef',
            Data.IMAGE_NAME: 'kth-azure-app',
        }

        result = tis.get_tag_without_commit_hash(data, registry_host="host.com")
        self.assertEqual(result, 'host.com/kth-azure-app:1.0.3')
