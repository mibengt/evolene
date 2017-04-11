__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data
from modules.util.environment import Environment
from modules.util.process import Process

class TagImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.IMAGE_NAME, Environment.REGISTRY_HOST]

    def get_required_data_keys(self):
        return [Data.LOCAL_IMAGE_ID, Data.IMAGE_VERSION]

    def run_step(self, data):
        image_id = data[Data.LOCAL_IMAGE_ID]
        image_version = data[Data.IMAGE_VERSION]
        image_name = Environment.get_image_name()
        registry = Environment.get_registry_host()
        tag = self.format_tag(registry, image_name, image_version)
        self.run_tag_command(tag, data)
        self.log.info('Tagged image "%s" with "%s"', image_id, tag)
        return data

    def run_tag_command(self, tag, data):
        cmd = 'docker tag {} {}'.format(data[Data.LOCAL_IMAGE_ID], tag)
        Process.run_with_output(cmd)

    def format_tag(self, registry, image_name, image_version):
        return '{}/{}:{}'.format(registry, image_name, image_version)
