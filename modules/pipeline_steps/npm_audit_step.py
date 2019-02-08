__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException
from modules.util import nvm

class NpmAuditStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        try:
            result = nvm.exec_npm_command(data, 'audit --json')
        except PipelineException as npm_ex:
            self.handle_step_error(
                'npm audit failed',
                npm_ex
            )
        audit_json = json.loads(result)
        self.log.debug('Audit result was "%s"', json.dumps(audit_json))
        return data
