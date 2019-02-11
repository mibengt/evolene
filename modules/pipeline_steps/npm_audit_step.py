__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data

class NpmAuditStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]

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
        self.approve_audit(data, audit_json)
        self.log.debug('Audit result was "%s"', json.dumps(audit_json))
        return data

    def approve_audit(self, data, audit_json):
        allow_criticals = False
        if pipeline_data.NPM_CONF_ALLOW_CRITICALS in data:
            allow_criticals = True
        criticals = self.get_criticals_from_audit(audit_json)
        if criticals > 0:
            self.log.debug('%s critical audit vulnerabilities found', criticals)
            if not allow_criticals:
                self.handle_step_error(
                    'Package contains %s critical vulnerability, aborting',
                    criticals
                )
            else:
                self.log.warning(
                    'Criticals exists, but ALLOW_CRITICALS set; continuing'
                )
        self.log.debug('No critical vulernabilities found')

    def get_criticals_from_audit(self, audit_json):
        try:
            return audit_json['metadata']['vulnerabilities']['critical']
        except KeyError as key_err:
            self.handle_step_error('Error when parsing npm audit output', key_err)      
 