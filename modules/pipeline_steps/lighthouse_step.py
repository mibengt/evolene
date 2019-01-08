__author__ = 'tinglev@kth.se'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class InstructionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        pass