__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class PushImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def run_step(self, data):
        data['pushed'] = True
        data['c'] = data['c'] + 1
        return data
