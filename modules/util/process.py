__author__ = 'tinglev'

import subprocess
import logging
from modules.util.exceptions import PipelineException

class Process(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def run_with_output(cmd):
        try:
            Process.log.debug('Running command with output: "%s"', cmd)
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            print(output)
            return output
        except subprocess.CalledProcessError as cpe:
            raise PipelineException('Shell command gave error with output: ```{}```'
                                    .format(cpe.output.rstrip('\n')))
