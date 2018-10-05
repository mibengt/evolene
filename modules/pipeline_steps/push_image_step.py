__author__ = 'tinglev'

from requests import get, HTTPError, ConnectTimeout, RequestException
from requests.auth import HTTPBasicAuth
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.exceptions import PipelineException
from modules.util.docker import Docker
from modules.util.environment import Environment

class PushImageStep(AbstractPipelineStep):

    def get_required_env_variables(self): #pragma: no cover
        return [Environment.REGISTRY_HOST,
                Environment.REGISTRY_USER,
                Environment.REGISTRY_PASSWORD]

    def get_required_data_keys(self): #pragma: no cover

        return [Data.IMAGE_VERSION, Data.IMAGE_NAME]

    def run_step(self, data):
        self.push_image(data)
        self.verify_push(data)
        return data
    
    def verify_push(self, data):
        tags = self.get_tags_from_registry(data)
        self.verify_image_version_in_tags(tags, data)

    def verify_image_version_in_tags(self, tags, data):
        if not data[Data.IMAGE_VERSION] in tags:
            self.log.error('Pushed tag could not be found in tag list on registry')
            raise PipelineException('Could not verify tag with remote registry')
        self.log.info('Found tag in tag list. Verification successful.')
        return True

    def get_tags_from_registry(self, data):
        url = self.create_registry_url(data)
        (user, password) = self.get_auth_tuple()
        response = self.call_api_endpoint(url, user, password)
        tags = self.get_tags_from_response(response)
        self.log.debug('Fetched tags: "%s"', tags)
        return tags

    def get_auth_tuple(self): #pragma: no cover
        return (Environment.get_registry_user(), Environment.get_registry_password())

    def create_registry_url(self, data):
        return 'https://{}/v2/{}/tags/list'.format(Environment.get_registry_host(),
                                                   data[Data.IMAGE_NAME])

    def get_tags_from_response(self, response): #pragma: no cover
        try:
            return response.json()['tags']
        except ValueError as json_err:
            raise PipelineException('Could not parse JSON response ("{}") from registry API: {}'
                                    .format(response.text, json_err))
        except KeyError:
            raise PipelineException('Registry API response contains no key "tags". Response was: {}'
                                    .format(response.text))

    def call_api_endpoint(self, url, user, password): #pragma: no cover
        try:
            return get(url, auth=HTTPBasicAuth(user, password))
        except HTTPError as http_err:
            raise PipelineException('HTTPError when calling registry API: {}'
                                    .format(http_err.response))
        except (ConnectTimeout, RequestException) as req_err:
            raise PipelineException('Timeout or request exception when calling registry API: {}'
                                    .format(req_err))

    def get_image_to_push(self, data):
        return '{}/{}:{}'.format(Environment.get_registry_host(),
                                 data[Data.IMAGE_NAME],
                                 data[Data.IMAGE_VERSION])
    
    def push_image(self, data):
        registry_image_name = self.get_image_to_push(data)
        Docker.push(registry_image_name)
        self.log.info('Pushed image "%s" to registry', registry_image_name)