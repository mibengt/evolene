__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment


class DoneStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.print_header()

        for item in data:
            print item
            
        return data

    def print_color(self, line, color='\033[0m'):
        print "{}{}\033[0m\n".format(color, line)
    
    def print_green(self, line):
        self.print_color(line, '\033[32m')

    def print_header(self):
        self.print_green("Built, tested and pushded to registry!")