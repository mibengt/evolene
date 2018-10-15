__author__ = 'tinglev'

import unittest
from modules.pipeline_steps.setup_step import SetupStep

class SetupStepTests(unittest.TestCase):

    def test_nothing(self):
        step = SetupStep()
        step.print_header()
