__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def run_step(self, data):
        data['image_version'] = True
        data['c'] = data['c'] + 1
        return data
