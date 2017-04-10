__author__ = 'tinglev'

from abc import ABCMeta, abstractmethod
import os
import logging
from modules.util.slack import Slack

class AbstractPipelineStep:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.log = logging.getLogger(self.get_step_name())
        self.next_step = None

    @abstractmethod
    def run_step(self, data):
        """ Should return data """
        pass

    @abstractmethod
    def get_required_env_variables(self):
        """ Should return a string array with the names of the environment
            variables required by the current step """
        pass

    @abstractmethod
    def get_required_data_keys(self):
        """ Should return a string array with the names of the keys
            that has to exist and have values in the data-object that
            is passed between build steps """
        pass

    def get_step_name(self):
        return self.__class__.__name__

    def _step_data_is_ok(self, data):
        for key in self.get_required_data_keys():
            if not key in data:
                err = '"{}" missing data key "{}"'.format(self.get_step_name(), key)
                self._handle_step_error(err)
                return False
        return True

    def _step_environment_ok(self):
        for env in self.get_required_env_variables():
            if not env in os.environ:
                err = '"{}" missing env variable "{}"'.format(self.get_step_name(), env)
                self._handle_step_error(err)
                return False
        return True

    def _handle_step_error(self, message, ex=None, fatal=True):
        error_func = self.log.error
        if fatal:
            error_func = self.log.fatal
        self._log_error(error_func, message, ex)
        self._report_error_to_slack(message)
        if fatal:
            exit(1)

    def _log_error(self, error_func, message, ex):
        if ex:
            error_func(message, exc_info=True)
        else:
            error_func(message)

    def _report_error_to_slack(self, message):
        #Slack.send_to_slack(channel, message)
        pass

    def run_pipeline_step(self, data):
        if not self._step_environment_ok():
            return data
        if not self._step_data_is_ok(data):
            return data
        self.log.debug('Running "%s"', self.get_step_name())
        self.run_step(data)
        if self.next_step:
            self.next_step.run_pipeline_step(data)
        return data

    def set_next_step(self, next_step):
        self.next_step = next_step
        return next_step
