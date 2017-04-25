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
