__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.process import Process
from modules.util.data import Data
from modules.util.exceptions import PipelineException
from modules.util import nvm

class InitNodeEnvironmentStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [Data.NPM_CONF_NODE_VERSION]

    def run_step(self, data):
        conf_version = data[Data.NPM_CONF_NODE_VERSION]
        self.log.debug('Configured node version is: "%s"', conf_version)
        try:
            self.get_nvm_installed_version(conf_version)
        except PipelineException as nvm_ex:
            if 'N/A' in str(nvm_ex):
                self.log.debug('Configured node version not installed; installing')
                self.install_version(conf_version)
            else:
                raise
        self.log.debug('Node version %s installed with nvm', conf_version)
        return data

    def get_nvm_installed_version(self, version):
        return nvm.nvm_run(f'nvm version {version}')

    def install_version(self, version):
        nvm.nvm_run(f'nvm install {version}')
