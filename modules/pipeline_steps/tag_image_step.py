__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data
from modules.util.environment import Environment
from modules.util import docker
from modules.util import image_version_util

class TagImageStep(AbstractPipelineStep):

    def get_required_env_variables(self): #pragma: no cover
        return [Environment.REGISTRY_HOST]

    def get_required_data_keys(self): #pragma: no cover
        return [pipeline_data.LOCAL_IMAGE_ID, pipeline_data.IMAGE_VERSION, pipeline_data.IMAGE_NAME]

    def run_step(self, data): #pragma: no cover

        self.tag(image_version_util.prepend_registry(image_version_util.get_image(data)), data)
        self.tag(image_version_util.prepend_registry(image_version_util.get_image_only_semver(data)), data)

        return data

    def tag(self, tag, data): #pragma: no cover
        docker.tag_image(data[pipeline_data.LOCAL_IMAGE_ID], tag)
        self.log.info('Tagged image "%s" with "%s"', data[pipeline_data.LOCAL_IMAGE_ID], tag)
