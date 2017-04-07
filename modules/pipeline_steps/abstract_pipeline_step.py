__author__ = 'tinglev'

from abc import ABCMeta, abstractmethod

class AbstractPipelineStep:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.successor = None

    @abstractmethod
    def run_step(self, data):
        """ Should return data """
        pass

    def run_pipeline(self, data):
        self.run_step(data)
        if self.successor:
            self.successor.run_pipeline(data)

    def set_successor(self, successor):
        self.successor = successor
