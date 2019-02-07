__author__ = 'tinglev'

import os
import unittest
from unittest import mock
from modules.util.environment import Environment
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
from modules.pipelines.npm_pipeline import NpmPipeline
import run

class RunTests(unittest.TestCase):

    def test_select_and_run_pipeline(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data/docker')
        DockerDeployPipeline.run_pipeline = mock.MagicMock()
        NpmPipeline.run_pipeline = mock.MagicMock()
        run.select_and_run_pipeline()
        DockerDeployPipeline.run_pipeline.assert_called_once()
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data/npm')
        run.select_and_run_pipeline()
        NpmPipeline.run_pipeline.assert_called_once()
