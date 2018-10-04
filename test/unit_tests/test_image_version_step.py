__author__ = 'tinglev'

import unittest
import os
from mock import patch
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.util.exceptions import PipelineException
from modules.util.environment import Environment

class ImageVersionStepTests(unittest.TestCase):

    @patch.object(ImageVersionStep, 'handle_step_error')
    def test_check_image_version(self, mock_handle_ex):
        ivs = ImageVersionStep()
        try:
            ivs.check_image_version('0.1')
            ivs.check_image_version('99.99')
        except PipelineException:
            self.fail('check_image_version raised an unexpected PipelineException')
        ivs.check_image_version('1.0.0')
        mock_handle_ex.assert_called_once()
        mock_handle_ex.reset_mock()
        ivs.check_image_version('1.')
        mock_handle_ex.assert_called_once()
        mock_handle_ex.reset_mock()
        ivs.check_image_version('1.0_test')
        mock_handle_ex.assert_called_once()
        mock_handle_ex.reset_mock()
        ivs.check_image_version('.0')
        mock_handle_ex.assert_called_once()
        mock_handle_ex.reset_mock()
        ivs.check_image_version('major.minor')
        mock_handle_ex.assert_called_once()
        mock_handle_ex.reset_mock()
        ivs.check_image_version('1.beta')
        mock_handle_ex.assert_called_once()

    def test_get_clamped_commit_hash(self):
        ivs = ImageVersionStep()
        os.environ[Environment.GIT_COMMIT] = '1234567'
        result = ivs.get_clamped_commit_hash()
        self.assertEqual(result, '1234567')
        os.environ[Environment.GIT_COMMIT] = '1234567890'
        result = ivs.get_clamped_commit_hash()
        self.assertEqual(result, '1234567')
        os.environ[Environment.GIT_COMMIT] = '1234567890'
        result = ivs.get_clamped_commit_hash(8)
        self.assertEqual(result, '12345678')
        os.environ[Environment.GIT_COMMIT] = '1234'
        result = ivs.get_clamped_commit_hash()
        self.assertEqual(result, '1234')

    def test_format_image_version_with_build_number_as_patch(self):
        ivs = ImageVersionStep()
        result = ivs.format_semver_version('1.2', 'ab12cb3', 123)
        self.assertEquals(result, '1.2.123_ab12cb3')

    def test_format_image_version_with_patch_in_docker_conf(self):
        ivs = ImageVersionStep()
        result = ivs.format_semver_version('1.2.321', 'ab12cb3', 999)
        self.assertEquals(result, '1.2.321_ab12cb3')

    def test_format_image_version_to_long(self):
        ivs = ImageVersionStep()
        self.assertRaises(ValueError, ivs.format_semver_version, '1.2.321.1', 'ab12cb3', 999)
