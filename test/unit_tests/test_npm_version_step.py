__author__ = 'tinglev'

import os
import unittest
from modules.pipeline_steps.npm_version_step import NpmVersionStep
from modules.pipeline_steps.load_package_json_step import LoadPackageJsonStep
from modules.util.data import Data
from modules.util.environment import Environment

class NpmVersionStepTests(unittest.TestCase):

    def test_run_step(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data/npm')
        load_step = LoadPackageJsonStep()
        step = NpmVersionStep()
        data = load_step.run_step({})
        result = step.run_step(data)
        self.assertEqual(result[Data.NPM_PACKAGE_VERSION], '1.0.0')
