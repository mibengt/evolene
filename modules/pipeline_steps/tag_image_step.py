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
        #docker tag $DOCKER_IMAGE_ID $REGISTRY_IMAGE_NAME:$IMAGE_VERSION
        #REGISTRY_IMAGE_NAME=$REGISTRY_HOST/$IMAGE_NAME
        Process.run_with_output('docker tag {} {}/{}:{}'
                                .format(data[Data.LOCAL_IMAGE_ID],
                                        Environment.get_registry_host(),
                                        Environment.get_image_name(),
                                        data[Data.IMAGE_VERSION]))
        return data
