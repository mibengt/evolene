__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util import docker
from modules.util import image_version_util
from modules.util import slack

class PushPublicImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION, pipeline_data.SEM_VER]

    def run_step(self, data):
        # Skip pushing on pull request testing
        if environment.get_pull_request_test():
            return data
        if environment.get_push_public():
            self.push_image(data)
            self.push_image_only_semver(data)
            self.push_latest(data)
        return data

    def push_latest(self, data):
        registry_image_name = image_version_util.prepend_registry(image_version_util.get_latest_tag(data))
        docker.push(registry_image_name)
        slack.on_successful_public_push(image_version_util.get_latest_tag(data), data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_SIZE])
        self.log.info('Pushed image "%s".', registry_image_name)

    def push_image(self, data):
        registry_image_name = image_version_util.prepend_registry(image_version_util.get_image(data))
        docker.push(registry_image_name)
        slack.on_successful_public_push(image_version_util.get_image(data), data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_SIZE])
        self.log.info('Pushed image "%s".', registry_image_name)

    def push_image_only_semver(self, data):
        registry_image_name = image_version_util.prepend_registry(image_version_util.get_image_only_semver(data))
        docker.push(registry_image_name)
        slack.on_successful_public_push(image_version_util.get_image_only_semver(data), data[pipeline_data.IMAGE_NAME], data[pipeline_data.IMAGE_SIZE])
        self.log.info('Pushed image "%s".', registry_image_name)
