__author__ = 'tinglev'

import unittest
from mock import patch
from modules.pipeline_steps.build_local_step import BuildLocalStep
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.docker import Docker

class BuildLocalStepTests(unittest.TestCase):

    def test_format_image_id(self):
        bls = BuildLocalStep()
        build_ouput = 'sha256:abcdefghijklmnopqrst'
        result = bls.format_image_id(build_ouput)
        self.assertEqual(result, 'abcdefghijkl')

    def test_get_image_size(self):
        bls = BuildLocalStep()
        grep_output = ('kthregistryv2.sys.kth.se/kth-azure-app   <none>              '
                       '0752187c9cce        13 days ago         107 MB')
        result = bls.get_image_size(grep_output)
        self.assertEqual(result, '107 MB')
        grep_output = ('kthregistryv2.sys.kth.se/kth-azure-app   <none>              '
                       '0752187c9cce        13 days ago         37.3 MB')
        result = bls.get_image_size(grep_output)
        self.assertEqual(result, '37.3 MB')
        grep_output = ''
        result = bls.get_image_size(grep_output)
        self.assertEqual(result, 'N/A')

    @patch.object(Docker, 'grep_image_id')
    @patch.object(AbstractPipelineStep, 'handle_step_error')
    def test_verify_built_image(self, mock_handle_error, mock_grep):
        bls = BuildLocalStep()
        mock_grep.return_value = ('kthregistryv2.sys.kth.se/kth-azure-app   <none>              '
                                  '0752187c9cce        13 days ago         107 MB')
        result = bls.verify_built_image('0752187c9cce')
        mock_grep.assert_called_once()
        self.assertEqual(result, mock_grep.return_value)
        mock_grep.reset_mock()
        mock_grep.return_value = ('kthregistryv2.sys.kth.se/kth-azure-app   <none>              '
                                  '0752187c9cce        13 days ago         107 MB')
        result = bls.verify_built_image('does_not_exist')
        mock_handle_error.assert_called_once()
