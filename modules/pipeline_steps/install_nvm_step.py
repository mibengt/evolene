__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.exceptions import PipelineException
from modules.util.process import Process
from modules.util import nvm

class InstallNvmStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)
        self.nvm_version = 'v0.34.0'

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        if os.path.isfile(nvm.NVM_DIR):
            self.log.debug('nvm is already installed, continuing')
        else:
            self.log.debug('nvm is not installed, installing now')
            cmd = (f'curl -o- https://raw.githubusercontent.com/creationix/nvm/'
                   f'{self.nvm_version}/install.sh | bash')
            try:
                Process.run_with_output(cmd)
            except PipelineException as install_ex:
                self.handle_step_error(
                    'Error while installing nvm',
                    install_ex
                )
            self.log.debug('nvm installed successfully')
