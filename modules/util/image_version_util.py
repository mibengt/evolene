__author__ = 'tinglev'

import re
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException
from modules.util.data import Data

class ImageVersionUtil(object):

    @staticmethod
    def is_major_minor_patch(image_version):
        if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', image_version):
            return False
        return True

    @staticmethod
    def is_major_minor_only(image_version):
        if not re.match(r'^[0-9]+\.[0-9]+$', image_version):
            return False
        return True

    @staticmethod
    def get_image(data):

        if data[Data.IMAGE_NAME] is None:
            raise PipelineException("Missing the name of the image.")

        if data[Data.IMAGE_VERSION] is None:
            raise PipelineException("Missing the version for the image.")

        return '{}:{}'.format(data[Data.IMAGE_NAME], data[Data.IMAGE_VERSION])

    @staticmethod
    def get_image_only_semver(data):

        if data[Data.IMAGE_NAME] is None:
            raise PipelineException("Missing the name of the image.")

        if data[Data.SEM_VER] is None:
            raise PipelineException("Missing the SemVer for the image.")

        return '{}:{}'.format(data[Data.IMAGE_NAME], data[Data.SEM_VER])

    @staticmethod
    def prepend_registry(image):
        return '{}/{}'.format(Environment.get_registry_host(), image)

    @staticmethod
    def get_image_uri(image):
        return ImageVersionUtil.prepend_registry(image)

    