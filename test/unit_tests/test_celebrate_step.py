__author__ = 'tinglev'

import unittest
import os
from modules.util.environment import Environment
from modules.util.data import Data
from modules.pipeline_steps.celebrate_step import CelebrateStep

class CelebrateStepTests(unittest.TestCase):

    def test_is_party(self):
        step = CelebrateStep()
        data = { Data.IMAGE_NAME: "app-name"}

        os.environ[Environment.BUILD_NUMBER] = "100"
        self.assertTrue("100" in step.get_party_message(data))

        os.environ[Environment.BUILD_NUMBER] = "500"
        self.assertTrue("500" in step.get_party_message(data))

        os.environ[Environment.BUILD_NUMBER] = "1000"
        self.assertTrue("1 000" in step.get_party_message(data))
