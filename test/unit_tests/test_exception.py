__author__ = 'tinglev'

import unittest
from modules.util.exceptions import PipelineException

class ExceptionsTests(unittest.TestCase):

    def test_no_slack_message(self):
        exception = PipelineException("Regular message")
        self.assertEqual(exception.slack_message, "Regular message")

    def test_slack_message(self):
        exception = PipelineException("Regular message", "Slack message")
        self.assertEqual(exception.slack_message, "Slack message")

    def test_slack_message_is_not_regular_message(self):
        exception = PipelineException("Regular message", "Slack message")
        self.assertEqual(str(exception), "Regular message")
