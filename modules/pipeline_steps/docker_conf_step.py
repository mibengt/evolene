__author__ = 'tinglev'

import re
import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class DockerConfPipelineStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        raw_lines = self.get_docker_conf_lines()
        print "******************"
        print raw_lines
        print "******************"
        env_lines = self.get_docker_conf_env_lines(raw_lines)
        missing_conf_vars = self.missing_conf_vars(env_lines)
        if missing_conf_vars:
            self.handle_step_error('Missing the following environment variables in docker.conf: {}'
                                   .format(missing_conf_vars))
        data = self.add_env_lines_to_data(env_lines, data)
        data[Data.DOCKER_CONF_FILE] = self.get_docker_conf_path()
        return data

    def clean_variable_value(self, value):
        return value.rstrip('"').lstrip('"')

    def add_env_lines_to_data(self, env_lines, data):
        try:
            for env in env_lines:
                self.log.debug("Adding /docker.conf value for: {}".format(env.split('=')[0]))
                data[env.split('=')[0]] = self.clean_variable_value(env.split('=')[1])
        except TypeError as t_err:
            self.log.warn('TypeError in add_env_lines_to_data: %s', t_err, exc_info=True)
            return data
                
        return data

    def get_docker_conf_path(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}/docker.conf'.format(stripped_root)

    def docker_conf_exists(self):
        return os.path.isfile(self.get_docker_conf_path())

    def get_docker_conf_env_lines(self, raw_lines):
        return [line for line in raw_lines
                if re.match(r'[^\s#="]+=(([^\s#="]+)|(".+"))$', line)]

    def get_docker_conf_lines(self):
        try:
            with open(self.get_docker_conf_path()) as d_conf:
                return d_conf.read().splitlines()
        except IOError as ioe:
            self.handle_step_error('Could not read docker.conf', ioe)

    def missing_conf_vars(self, lines):
        try:
            required = [Environment.IMAGE_NAME, Data.IMAGE_VERSION]
            variables = [line.split('=')[0] for line in lines]
            missing = [req for req in required if req not in variables]
        except TypeError as t_err:
            self.log.warn('TypeError in missing_conf_vars: %s', t_err, exc_info=True)
            return required
        return missing
