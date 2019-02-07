__author__ = 'tinglev'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.file_util import FileUtil
from modules.util.data import Data

class LoadPackageJsonStep(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        package_content = FileUtil.read_as_string('/package.json')
        if package_content:
            data[Data.PACKAGE_JSON] = json.loads(package_content)
        return data
