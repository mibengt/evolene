__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class DockerConfPipelineStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return ['PROJECT_ROOT_PATH']

    def run_step(self, data):
        data['path'] = os.environ['PROJECT_ROOT_PATH']
        data['conf'] = True
        data['c'] = data['c'] + 1
        return data

