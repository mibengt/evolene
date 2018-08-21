__author__ = 'tinglev'

import subprocess
import logging
from modules.util.exceptions import PipelineException

class Process(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def run_with_output(cmd, data):
        try:
            Process.log.debug('Running command with output: "%s"', cmd)
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        except subprocess.CalledProcessError as cpe:
            message = "Shell command gave error with output: {}".format(cpe.output)
            if data:
                message = "*{}* failed: \n{}".format(data[Data.IMAGE_NAME], cpe.output))

            raise PipelineException(message)
