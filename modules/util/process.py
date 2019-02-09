__author__ = 'tinglev'

import subprocess
import logging
import sys
from modules.util.exceptions import PipelineException

def run_with_output(cmd):
    log = logging.getLogger(__name__)
    try:
        log.debug('Running command with output: "%s"', cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if output:
            return output.decode('utf-8')

    except subprocess.CalledProcessError as cpe:
        if cpe.output:
            raise PipelineException(cpe.output.decode('utf-8'))
        raise PipelineException(f"{str(cpe)}")
    except:
        raise PipelineException(
            "Unabled exception. {}".format(sys.exc_info()[0]))
