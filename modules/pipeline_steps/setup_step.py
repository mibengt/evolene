__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.print_util import PrintUtil


class SetupStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.SLACK_CHANNELS, Environment.SLACK_WEB_HOOK]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        self.print_header()
        return data

    def print_header(self):
        PrintUtil.black("                                                    ")
        PrintUtil.pink("  ______                   _                        ")
        PrintUtil.pink(" |  ____|                 | |                       ")
        PrintUtil.pink(" | |__    __   __   ___   | |   ___   _ __     ___  ")
        PrintUtil.pink(" |  __|   \ \ / /  / _ \  | |  / _ \ | '_ \   / _ \ ")
        PrintUtil.pink(" | |____   \ V /  | (_) | | | |  __/ | | | | |  __/ ")
        PrintUtil.pink(" |______|   \_/    \___/  |_|  \___| |_| |_|  \___| ")
        PrintUtil.black("                                                    ")
        PrintUtil.black("                                                    ")
        PrintUtil.black("****************************************************")
        PrintUtil.black(" Help make Evolene better!                          ")
        PrintUtil.black(" https://gita.sys.kth.se/Infosys/evolene            ")
        PrintUtil.black("****************************************************")
        PrintUtil.black("                                                    ")
