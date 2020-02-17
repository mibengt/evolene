__author__ = 'tinglev'

import unittest
import time
from mock import patch, call
from modules.pipeline_steps.dry_run_step import DryRunStep
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, docker

class DryRunStepTests(unittest.TestCase):

    def test_is_running(self):
        drs = DryRunStep()
        self.assertFalse(drs.is_running(None))
        self.assertFalse(drs.is_running(''))
        self.assertFalse(drs.is_running('created'))
        self.assertTrue(drs.is_running('running'))

    def test_is_creating(self):
        drs = DryRunStep()
        self.assertFalse(drs.is_creating(None))
        self.assertFalse(drs.is_creating(''))
        self.assertFalse(drs.is_creating('running'))
        self.assertTrue(drs.is_creating('created'))

    @patch.object(DryRunStep, 'get_container_status')
    @patch.object(time, 'sleep')
    def test_wait_for_container_created(self, mock_sleep, mock_status):
        mock_status.side_effect = ['created', 'created', 'running']
        drs = DryRunStep()
        result = drs.wait_for_container_created('test')
        calls = [call(5), call(5)]
        mock_sleep.assert_has_calls(calls)
        self.assertEqual(result, 'running')

    @patch.object(DryRunStep, 'start_container')
    @patch.object(DryRunStep, 'stop_container')
    @patch.object(DryRunStep, 'wait_for_container_created')
    @patch.object(AbstractPipelineStep, 'handle_step_error')
    def test_run_step(self, mock_handle_err, mock_wait, mock_stop, mock_start):
        DryRunStep.DRY_RUN_COMPOSE_FILENAME = 'not-available'
        mock_wait.return_value = 'running'
        mock_start.return_value = 'test_container_id'
        drs = DryRunStep()
        data = {}
        data[pipeline_data.LOCAL_IMAGE_ID] = 'image_id'
        result = drs.run_step(data)
        self.assertEqual(result, data)
        mock_start.assert_called_once()
        mock_wait.assert_called_once()
        mock_stop.assert_called_once()
        mock_handle_err.assert_not_called()
        mock_start.reset_mock()
        mock_stop.reset_mock()
        mock_wait.reset_mock()
        mock_handle_err.reset_mock()
        mock_wait.return_value = 'stopped'
        result = drs.run_step(data)
        mock_start.assert_called_once()
        mock_wait.assert_called_once()
        mock_handle_err.assert_called_once()
        mock_stop.assert_called_once()

    @patch.object(docker, 'run_dry_run_compose')
    def test_compose_dry_run(self, mock_dry_run):
        DryRunStep.DRY_RUN_COMPOSE_FILENAME = '/docker-compose-dry-run.yml'
        drs = DryRunStep()
        data = {}
        data[pipeline_data.LOCAL_IMAGE_ID] = 'image_id'
        drs.run_step(data)
        mock_dry_run.assert_called_once()
