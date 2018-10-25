__author__ = 'tinglev'

import logging
from modules.util.process import Process
from modules.util.exceptions import PipelineException

class GitUtil(object):

    log = logging.getLogger(__name__)

    @staticmethod
    def get_commiter_email():
        result = None
        try:
            result = Process.run_with_output("git log -1 --pretty=format:'%ae'")
        except PipelineException as ple:
            GitUtil.log.debug('Could not find any e-mail for the commiter in git log. "%s"', ple)
        return result
