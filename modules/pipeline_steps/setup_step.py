__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment

class SetupStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.SLACK_CHANNELS, Environment.SLACK_WEB_HOOK]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        return data
