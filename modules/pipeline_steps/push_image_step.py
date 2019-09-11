__author__ = 'tinglev'

from requests import get, HTTPError, ConnectTimeout, RequestException
from requests.auth import HTTPBasicAuth
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import pipeline_data
from modules.util.exceptions import PipelineException
from modules.util import docker
from modules.util import image_version_util
from modules.util import slack

class PushImageStep(AbstractPipelineStep):

    def get_required_env_variables(self): #pragma: no cover
        return [environment.REGISTRY_HOST,
                environment.REGISTRY_USER,
                environment.REGISTRY_PASSWORD]

    def get_required_data_keys(self): #pragma: no cover
        return [pipeline_data.IMAGE_VERSION, pipeline_data.IMAGE_NAME]

    def run_step(self, data):
        # Skip pushing on pull request testing
        if environment.get_pull_request_test():
            return data
        if not environment.get_push_public():
            self.push_image(data)
            self.verify_push(data)
        return data

    def verify_push(self, data):
        tags = self.get_tags_from_registry(data)
        self.verify_image_version_in_tags(tags, data)

    def verify_image_version_in_tags(self, tags, data):
        if not data[pipeline_data.IMAGE_VERSION] in tags:
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
        return (environment.get_registry_user(), environment.get_registry_password())

    def create_registry_url(self, data):
        return 'https://{}/v2/{}/tags/list'.format(environment.get_registry_host(),
                                                   data[pipeline_data.IMAGE_NAME])

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
            response = get(url, auth=HTTPBasicAuth(user, password))
            if response.status_code == 200:
                return response
            if response.status_code == 404:
                raise PipelineException('Could not find any images in registry for {}'.format(url))
                        
        except HTTPError as http_err:
            raise PipelineException('HTTPError when calling registry API: {}'.format(http_err.response))
        except (ConnectTimeout, RequestException) as req_err:
            raise PipelineException('Timeout or request exception when calling registry API: {}'.format(req_err))
    
    def get_image_to_push(self, data):
        return image_version_util.prepend_registry(image_version_util.get_image(data))

    def push_image(self, data):
        registry_image_name = self.get_image_to_push(data)
        docker.push(registry_image_name)
        slack.on_successful_private_push(image_version_util.get_image(data), data[pipeline_data.IMAGE_SIZE])
        self.log.info('Pushed image %s to KTH registry.', registry_image_name)