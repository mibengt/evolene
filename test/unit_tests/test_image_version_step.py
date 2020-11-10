__author__ = 'tinglev'

import unittest
from unittest import mock
import os
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.util import environment

class ImageVersionStepTests(unittest.TestCase):

    def test_format_image_version_with_build_number_as_patch(self):
        os.environ[environment.GIT_BRANCH] = 'master'
        ivs = ImageVersionStep()
        result = ivs.get_sem_ver('1.2', 123)
        self.assertEqual(result, '1.2.123')

    def test_format_image_version_to_long(self):
        os.environ[environment.GIT_BRANCH] = 'master'
        ivs = ImageVersionStep()
        ImageVersionStep.handle_step_error = mock.MagicMock()
        ivs.get_sem_ver('1.2.321', 1)
        ImageVersionStep.handle_step_error.assert_called_once()
