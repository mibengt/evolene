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