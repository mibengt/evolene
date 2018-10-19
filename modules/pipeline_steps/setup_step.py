__author__ = 'tinglev'

import os
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

    def print_header(self):
        print (
            "                                                    \n"
            "  ______                   _                        \n"
            " |  ____|                 | |                       \n"
            " | |__    __   __   ___   | |   ___   _ __     ___  \n" 
            " |  __|   \ \ / /  / _ \  | |  / _ \ | '_ \   / _ \ \n"
            " | |____   \ V /  | (_) | | | |  __/ | | | | |  __/ \n"
            " |______|   \_/    \___/  |_|  \___| |_| |_|  \___| \n"
            "                                                    \n"
            "****************************************************\n"
            " Help make Evolene better!                          \n"
            " https://gita.sys.kth.se/Infosys/evolene            \n"
            "****************************************************\n"
            "                                                    \n"
        )
        print "GIT_COMMITTER_NAME: {}".format(os.environ.get("GIT_COMMITTER_NAME"))
        print "GIT_AUTHOR_NAME: {}".format(os.environ.get("GIT_AUTHOR_NAME"))
        print "GIT_COMMITTER_EMAIL: {}".format(os.environ.get("GIT_COMMITTER_EMAIL"))
        print "GIT_AUTHOR_EMAIL: {}".format(os.environ.get("GIT_AUTHOR_EMAIL"))
                                                   
                                                   