__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException
from modules.util.data import Data
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

    def approve_audit(self, data, audit_json):
        allow_criticals = data[Data.NPM_CONF_ALLOW_CRITICALS]
        criticals = audit_json['metadata']['vulnerabilities']['critical']
        if criticals > 0:
            self.log.debug('%s critical audit vulnerabilities found', criticals)
            if not allow_criticals:
                self.handle_step_error(
                    'Package contains %s critical vulnerability, aborting',
                    criticals
                )
            else:
                self.log.debug('ALLOW_CRITICALS set, continuing')
        self.log.debug('No critical vulernabilities found')
 