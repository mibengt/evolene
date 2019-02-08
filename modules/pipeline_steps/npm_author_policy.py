__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data

class NpmAuthorPolicy(AbstractPipelineStep):

    def __init__(self):
        AbstractPipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [Data.PACKAGE_JSON]

    def run_step(self, data):
        if not 'author' in data[Data.PACKAGE_JSON]:
            self.handle_step_error(
                '"author" must be set in package.json'
            )
        if (not 'name' in data[Data.PACKAGE_JSON]['author'] or
                not 'email' in data[Data.PACKAGE_JSON]['author']):
            self.handle_step_error(
                '"name" and "email" must be set for "author" in package.json'
            )
        self.log.debug('Author has name and email in package.json, continuing')
        return data
