__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data
from modules.util.environment import Environment
from modules.util.docker import Docker

class TagImageStep(AbstractPipelineStep):

    def get_required_env_variables(self): #pragma: no cover
        return [Environment.REGISTRY_HOST]

    def get_required_data_keys(self): #pragma: no cover
        return [Data.LOCAL_IMAGE_ID, Data.IMAGE_VERSION, Data.IMAGE_NAME]

    def run_step(self, data): #pragma: no cover
        self.run_tag_command(self.get_default_tag(data), data)
        if Environment.extra_tag_without_commit_hash():
            self.run_tag_command(self.get_tag_without_commit_hash(data), data)

        return data

    def get_default_tag(self, data, registry_host=Environment.get_registry_host()):
        return '{}/{}:{}'.format(registry_host,
                                 data[Data.IMAGE_NAME],
                                 data[Data.IMAGE_VERSION])
        
    def get_tag_without_commit_hash(self, data, registry_host=Environment.get_registry_host()):
        return '{}/{}:{}'.format(registry_host,
                                 data[Data.IMAGE_NAME],
                                 data[Data.SEM_VER])

    def run_tag_command(self, tag, data): #pragma: no cover
        Docker.tag_image(data[Data.LOCAL_IMAGE_ID], tag)
        self.log.info('Tagged image "%s" with "%s"', data[Data.LOCAL_IMAGE_ID], tag)
