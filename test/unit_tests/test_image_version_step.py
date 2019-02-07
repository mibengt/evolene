__author__ = 'tinglev'

import unittest
import os
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.util.environment import Environment

class ImageVersionStepTests(unittest.TestCase):

    def test_get_commit_hash_clamped(self):
        ivs = ImageVersionStep()
        os.environ[Environment.GIT_COMMIT] = '1234567'
        result = ivs.get_commit_hash_clamped()
        self.assertEqual(result, '1234567')
        os.environ[Environment.GIT_COMMIT] = '1234567890'
        result = ivs.get_commit_hash_clamped()
        self.assertEqual(result, '1234567')
        os.environ[Environment.GIT_COMMIT] = '1234567890'
        result = ivs.get_commit_hash_clamped(8)
        self.assertEqual(result, '12345678')
        os.environ[Environment.GIT_COMMIT] = '1234'
        result = ivs.get_commit_hash_clamped()
        self.assertEqual(result, '1234')

    def test_format_image_version_with_build_number_as_patch(self):
        ivs = ImageVersionStep()
        result = ivs.get_sem_ver('1.2', 123)
        self.assertEqual(result, '1.2.123')

    def test_format_image_version_to_long(self):
        ivs = ImageVersionStep()
        try:
            ivs.get_sem_ver('1.2.321', 1)
            self.assertEqual("", "Should not be allowed to come here.")
        except Exception:
            pass
