__author__ = 'tinglev'

class PipelineException(Exception):

    def __init__(self, message):
        super(PipelineException, self).__init__(message)
