__author__ = 'tinglev'

import unittest
from modules.util import semver
from modules.util.exceptions import PipelineException

class SemverTests(unittest.TestCase):

    def test_get_patch(self):
        self.assertEquals(semver.get_patch("1.2.3"), 3)
        self.assertEquals(semver.get_patch("2.2.3"), 3)
        self.assertEquals(semver.get_patch("2.2"), 0)
        with self.assertRaises(PipelineException):
            semver.get_patch(None)


    def test_get_major_minor(self):
        self.assertEquals(semver.get_major_minor("1.2.3"), "1.2")
        self.assertEquals(semver.get_major_minor("2.2.3"), "2.2")
        self.assertEquals(semver.get_major_minor("2.2"), "2.2")

    def test_get_next(self):
        self.assertEquals(semver.get_next("1.2.3"), "1.2.4")
        self.assertEquals(semver.get_next("2.2.3"), "2.2.4")
        self.assertEquals(semver.get_next("2.2"), "2.2.0")
        with self.assertRaises(PipelineException):
            semver.get_next(None)
