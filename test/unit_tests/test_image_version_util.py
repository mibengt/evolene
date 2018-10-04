__author__ = 'tinglev'

import unittest

from modules.util.image_version_util import ImageVersionUtil
from modules.util.environment import Environment

class ImageVersionUtilTests(unittest.TestCase):

    def test_patch_exists(self):
        self.assertTrue(ImageVersionUtil.is_major_minor_patch( '1.2.321'))

    def test_full_version_to_short(self):
        self.assertFalse(ImageVersionUtil.is_major_minor_patch( '1.2.321.1337'))

    def test_version_to_long(self):
        self.assertFalse(ImageVersionUtil.is_major_minor_patch( '1.2.321.1337'))

    def test_not_exists(self):
        self.assertFalse(ImageVersionUtil.is_major_minor_only( '1.2.321'))

    def test_major_minor_version_to_short(self):
        self.assertFalse(ImageVersionUtil.is_major_minor_patch( '1.2.321.1337'))

