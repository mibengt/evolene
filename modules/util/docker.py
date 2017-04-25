__author__ = 'tinglev'

from modules.util.process import Process
from modules.util.environment import Environment

class Docker(object):

    @staticmethod
    def build():
        return Process.run_with_output('docker build -q {}'
                                       .format(Environment.get_project_root()))

    @staticmethod
    def grep_image_id(image_id):
        return Process.run_with_output('docker image ls | grep {}'
                                       .format(image_id))

    @staticmethod
    def get_container_status(container_id):
        return Process.run_with_output('docker inspect --format=\'{{{{.State.Status}}}}\' {}'
                                       .format(container_id)).rstrip()

    @staticmethod
    def run(image_id):
        return Process.run_with_output('docker run -d {}'.format(image_id)).rstrip()

    @staticmethod
    def stop_and_remove_container(container_id):
        Process.run_with_output('docker rm -f {}'.format(container_id))
