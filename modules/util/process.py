__author__ = 'tinglev'

import subprocess
import logging
from modules.util.exceptions import PipelineException
from modules.util.data import Data

class Process(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def run_with_output(cmd):
        try:
            Process.log.debug('Running command with output: "%s"', cmd)
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        except subprocess.CalledProcessError as cpe:
            if cpe:
                if cpe.output:
                    raise PipelineException(cpe.output)
            
            raise PipelineException("Opps had an unhandled error while building :( {}".format(cpe))
            