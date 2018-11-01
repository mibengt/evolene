__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment


class SetupStep(AbstractPipelineStep):



    def get_required_env_variables(self):
        return [Environment.SLACK_CHANNELS, Environment.SLACK_WEB_HOOK]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.print_header()
        return data

    def color(self, line, color='\033[0m'):
        print "{}{}\033[0m\n".format(color, line)
    
    def print_black(self, line):
        self.color(line, color='\033[95m')

    def print_pink(self, line):
        self.print_black(line, color='\033[95m')

    def print_header(self):
        self.print_black("                                                    ")
        self.print_pink("  ______                   _                        ")
        self.print_pink(" |  ____|                 | |                       ")
        self.print_pink(" | |__    __   __   ___   | |   ___   _ __     ___  ")
        self.print_pink(" |  __|   \ \ / /  / _ \  | |  / _ \ | '_ \   / _ \ ")
        self.print_pink(" | |____   \ V /  | (_) | | | |  __/ | | | | |  __/ ")
        self.print_pink(" |______|   \_/    \___/  |_|  \___| |_| |_|  \___| ")
        self.print_black("                                                    ")
        self.print_black("                                                    ")
        self.print_black("****************************************************")
        self.print_black(" Help make Evolene better!                          ")
        self.print_black(" https://gita.sys.kth.se/Infosys/evolene            ")
        self.print_black("****************************************************")
        self.print_black("                                                    ")
