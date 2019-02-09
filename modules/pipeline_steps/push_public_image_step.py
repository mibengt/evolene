__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util import pipeline_data
from modules.util import docker
from modules.util.image_version_util import ImageVersionUtil
from modules.util.slack import Slack

class PushPublicImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PUSH_PUBLIC]

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION, pipeline_data.SEM_VER]

    def run_step(self, data):
        self.push_image(data)
        self.push_image_only_semver(data)

        return data

    def push_image(self, data):
        registry_image_name = ImageVersionUtil.prepend_registry(ImageVersionUtil.get_image(data))
        docker.push(registry_image_name)
        Slack.on_successful_public_push(ImageVersionUtil.get_image(data), data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_SIZE])
        self.log.info('Pushed image "%s".', registry_image_name)

    def push_image_only_semver(self, data):
        registry_image_name = ImageVersionUtil.prepend_registry(ImageVersionUtil.get_image_only_semver(data))
        docker.push(registry_image_name)
        Slack.on_successful_public_push(ImageVersionUtil.get_image_only_semver(data), data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_SIZE])
        self.log.info('Pushed image "%s".', registry_image_name)
