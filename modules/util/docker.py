__author__ = 'tinglev'

from modules.util.process import Process
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException
from modules.util.data import Data

class Docker(object):

    UNIT_TEST_COMPOSE_FILENAME = 'docker-compose-unit-tests.yml'
    INTEGRATION_TEST_COMPOSE_FILENAME = 'docker-compose-integration-tests.yml'

    @staticmethod
    def build(labels=None):
        build_cmd = 'docker build --quiet'
        if labels:
            for label in labels:
                build_cmd = '{} --label {}'.format(build_cmd, label)
        return Process.run_with_output('{} {}'
                                       .format(build_cmd, 
                                               Environment.get_project_root()))

    @staticmethod
    def grep_image_id(image_id):
        try:
            return Process.run_with_output('docker images | grep {}'
                                           .format(image_id))
        except PipelineException as pipeline_err:
            if '""' in pipeline_err.message:
                # We got an empty output, which means that the grep failed
                # which in turn means that no image was found, return None
                return None
            raise

    @staticmethod
    def get_container_status(container_id):
        return Process.run_with_output('docker inspect --format=\'{{{{.State.Status}}}}\' {}'
                                       .format(container_id)).rstrip()

    @staticmethod
    def run(image_id):
        return Process.run_with_output('docker run -d {}'.format(image_id)).rstrip()

    @staticmethod
    def stop_and_remove_container(container_id):
        return Process.run_with_output('docker rm -f {}'.format(container_id))

    @staticmethod
    def tag_image(image_id, tag):
        return Process.run_with_output('docker tag {} {}'.format(image_id, tag))

    @staticmethod
    def push(registry_image_name):
        return Process.run_with_output('docker push {}'.format(registry_image_name))

    @staticmethod
    def inspect_image(image_id):
        return Process.run_with_output('docker image inspect {}'.format(image_id))

    @staticmethod
    def pull(image_name):
        return Process.run_with_output('docker pull {}'.format(image_name))

    @staticmethod
    def run_unit_test_compose(compose_test_file, data):
        return Docker.run_test(compose_test_file, data)

    @staticmethod
    def run_integration_tests(compose_test_file, data):
        return Docker.run_test(compose_test_file, data)

    @staticmethod
    def run_test(compose_test_file, data):
        cmd = 'LOCAL_IMAGE_ID={} IMAGE_NAME={} IMAGE_VERSION={} docker-compose --file {} up --build --abort-on-container-exit'.format(
                                                data[Data.LOCAL_IMAGE_ID],
                                                data[Data.IMAGE_NAME],
                                                data[Data.IMAGE_VERSION],
                                                compose_test_file)
        return Process.run_with_output(cmd)
