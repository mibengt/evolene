__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class TestImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        data['test_image'] = True
        data['c'] = data['c'] + 1
        return data
