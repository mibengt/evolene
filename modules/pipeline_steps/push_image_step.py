__author__ = 'tinglev'

from requests import get, HTTPError, ConnectTimeout, RequestException
from requests.auth import HTTPBasicAuth
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.process import Process
from modules.util.exceptions import PipelineException

class PushImageStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.REGISTRY_HOST,
                Environment.IMAGE_NAME,
                Environment.REGISTRY_USER,
                Environment.REGISTRY_PASSWORD]

    def get_required_data_keys(self):
        return [Data.IMAGE_VERSION]

    def run_step(self, data):
        registry_host = Environment.get_registry_host()
        image_name = Environment.get_image_name()
        self.push_image(registry_host, image_name)
        tags = self.get_tags_from_registry(registry_host, image_name)
        self.verify_tags(tags, data)
        return data

    def verify_tags(self, tags, data):
        if not data[Data.IMAGE_VERSION] in tags:
            self.log.error('Pushed tag could not be found in tag list on registry')
            raise PipelineException('Could not verify tag with remote registry')
        self.log.info('Found tag in tag list. Verification successful.')

    def get_tags_from_registry(self, registry_host, image_name):
        url = self.create_registry_url(registry_host, image_name)
        (user, password) = self.get_auth_tuple()
        response = self.call_api_endpoint(url, user, password)
        tags = self.get_tags_from_response(response)
        self.log.debug('Fetched tags: "%s"', tags)
        return tags

    def get_auth_tuple(self):
        return (Environment.get_registry_user(), Environment.get_registry_password())

    def create_registry_url(self, registry_host, image_name):
        return 'https://{}/v2/{}/tags/list'.format(registry_host, image_name)

    def get_tags_from_response(self, response):
        try:
            return response.json()['tags']
        except ValueError as json_err:
            raise PipelineException('Could not parse JSON response ("{}") from registry API: {}'
                                    .format(response.text, json_err))
        except KeyError:
            raise PipelineException('Registry API response contains no key "tags". Response was: {}'
                                    .format(response.text))

    def call_api_endpoint(self, url, user, password):
        try:
            return get(url, auth=HTTPBasicAuth(user, password))
        except HTTPError as http_err:
            raise PipelineException('HTTPError when calling registry API: {}'
                                    .format(http_err.response))
        except (ConnectTimeout, RequestException) as req_err:
            raise PipelineException('Timeout or request exception when calling registry API: {}'
                                    .format(req_err))

    def get_image_to_push(self, registry_host, image_name):
        return '{}/{}'.format(registry_host, image_name)

    def push_image(self, registry_host, image_name):
        registry_image_name = self.get_image_to_push(registry_host, image_name)
        cmd = 'docker push {}'.format(registry_image_name)
        Process.run_with_output(cmd)
        self.log.info('Pushed image to registry')
