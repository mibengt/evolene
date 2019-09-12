__author__ = 'tinglev'

class PipelineException(Exception):

    def __init__(self, message, slack_message=None):
        super(PipelineException, self).__init__(message)
        self.pipeline_data = {}

        if slack_message:
            self.slack_message = slack_message
        else:
            self.slack_message = message

    def get_data(self):
        return self.pipeline_data

    def set_data(self, pipeline_data):
        self.pipeline_data = pipeline_data
