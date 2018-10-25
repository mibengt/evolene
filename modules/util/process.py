__author__ = 'tinglev'

import subprocess
import logging
import sys
from modules.util.exceptions import PipelineException


class Process(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def run_with_output(cmd):
        try:
            Process.log.debug('Running command with output: "%s"', cmd)
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        except subprocess.CalledProcessError as cpe:
            if cpe.output:
                raise PipelineException(cpe.output)
            raise PipelineException("{}".format(cpe))
        except:
            raise PipelineException(
                "Unabled exception. {}".format(sys.exc_info()[0]))
