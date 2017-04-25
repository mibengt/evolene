__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.tag_image_step import TagImageStep

class TagImageStepTests(unittest.TestCase):

    def test_format_tag(self):
        tis = TagImageStep()
        result = tis.format_tag('kthregistryv2.sys.kth.se', 'kth-azure-app', '1.0')
        self.assertEqual(result, 'kthregistryv2.sys.kth.se/kth-azure-app:1.0')
