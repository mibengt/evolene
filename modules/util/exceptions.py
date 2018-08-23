__author__ = 'tinglev'

class PipelineException(Exception):

    slack_message = None
    def __init__(self, message, slack_message=None):
        super(PipelineException, self).__init__(message)
        
        if slack_message:
            self.slack_message = slack_message
        else:
            self.slack_message = message
