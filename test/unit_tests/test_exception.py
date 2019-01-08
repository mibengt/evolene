__author__ = 'tinglev'

import os
import unittest

from modules.util.exceptions import PipelineException


class ExceptionsTests(unittest.TestCase):

    def test_no_slack_message(self):
        exception = PipelineException("Regular message")
        self.assertEquals(exception.slack_message, "Regular message")

    def test_slack_message(self):
        exception = PipelineException("Regular message", "Slack message")
        self.assertEquals(exception.slack_message, "Slack message")

    def test_slack_message_is_not_regular_message(self):
        exception = PipelineException("Regular message", "Slack message")
        self.assertEquals(str(exception), "Regular message")
