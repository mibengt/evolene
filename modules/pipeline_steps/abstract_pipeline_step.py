__author__ = 'tinglev'

from abc import ABCMeta, abstractmethod
import os
import logging

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

    def get_step_name(self):
        return self.__class__.__name__

    def step_environment_ok(self):
        for env in self.get_required_env_variables():
            if not env in os.environ:
                err = '"{}" missing env variable "{}"'.format(self.get_step_name(), env)
                self._handle_step_error(err)
                return False
        return True

    def _handle_step_error(self, message, ex=None):
        if ex:
            self.log.error(message, exc_info=True)
        else:
            self.log.error(message)
        # TODO: Report error to Slack

    def run_pipeline_step(self, data):
        if not self.step_environment_ok():
            return data
        self.run_step(data)
        if self.next_step:
            self.next_step.run_pipeline_step(data)
        return data

    def set_next_step(self, next_step):
        self.next_step = next_step
        return next_step
