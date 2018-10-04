__author__ = 'tinglev'

import re
from modules.util.environment import Environment

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
    def is_valid(image_version):
        if ImageVersionUtil.use_patch_from_docker_conf():
            return ImageVersionUtil.is_major_minor_patch(image_version)
        return ImageVersionUtil.is_major_minor_only(image_version)
    
    @staticmethod
    def use_patch_from_docker_conf():
        if Environment.get_build_number() is None:
            return False

        if Environment.get_build_number() == "docker.conf":
            return True
        
        return False