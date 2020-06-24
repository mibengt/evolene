__author__ = 'tinglev'

import unittest
from modules.util import semver

class SemverTests(unittest.TestCase):

    def test_get_next(self):
        next = semver.get_next("1.2.3")
        self.assertEquals(next, "1.2.4")
