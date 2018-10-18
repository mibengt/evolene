__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.file_util import FileUtil

class DockerConfPipelineStep(AbstractPipelineStep):

    FILE_DOCKER_CONF = "/docker.conf"

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        
        data[Data.DOCKER_CONF_FILE] = FileUtil.get_absolue_path(DockerConfPipelineStep.FILE_DOCKER_CONF)

        conf_lines = self.trim(FileUtil.get_lines(DockerConfPipelineStep.FILE_DOCKER_CONF))

        if self.has_missing_conf_vars(conf_lines):
            self.handle_step_error('Missing the following configuration variables in `/docker.conf`: {}'
                                   .format(self.get_missing_conf_vars))

        data = self.add_conf_vars(conf_lines, data)
        
        return data

    def clean_variable_value(self, value):
        return value.rstrip('"').lstrip('"')

    def add_conf_vars(self, env_lines, data):
        try:
            for env in env_lines:
                self.log.debug("Adding /docker.conf value for: {}".format(env.split('=')[0]))
                data[env.split('=')[0]] = self.clean_variable_value(env.split('=')[1])

        except TypeError as t_err:
            self.log.warn('TypeError in add_conf_vars: %s', t_err, exc_info=True)
            return data
                
        return data

    def trim(self, raw_lines):
        return [line for line in raw_lines
                if re.match(r'[^\s#="]+=(([^\s#="]+)|(".+"))$', line)]

    def has_missing_conf_vars(self, lines):
        if self.get_missing_conf_vars(lines):
            return True
        return False

    def get_missing_conf_vars(self, lines):
        try:
            required = [Environment.IMAGE_NAME, Data.IMAGE_VERSION]
            variables = [line.split('=')[0] for line in lines]
            missing = [req for req in required if req not in variables]
        except TypeError as t_err:
            self.log.warn('TypeError in missing conf vars: %s', t_err, exc_info=True)
            return required
        return missing
