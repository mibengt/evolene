__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.slack import Slack
import logging

class FromImageStep(AbstractPipelineStep):

    SUPPORTED_IMAGES = {
        "kth-os": [ "3.8" ],
        "kth-nodejs": [ "8.11", "9.11"],
        "kth-nodejs-web": [ "2.4" ],
        "kth-nodejs-api": [ "2.4" ],
        "oracle": [ ],
        "redis": ["*"]
    }

    def __init__(self, supported_images=None):
        self.log = logging.getLogger(self.get_step_name())
        if supported_images:
            self.SUPPORTED_IMAGES = supported_images

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        from_line = self.get_from_line()
        log_prefix = "{}:{}".format(data[Data.IMAGE_NAME], data[Data.COMMIT_HASH])
        if self.validate(from_line, log_prefix):
            self.log.debug("'FROM:' statement '{}' in Dockerfile is valid.".format(from_line))
        else:
            message = "*{}* Dockerfile uses an unsupported and possibly unsecure `{}` image, please upgrade!".format(log_prefix, from_line)
            self.log.warn(message)
            Slack.on_warning(message)
        
        return data

    def validate(self, from_line, log_prefix):
        for image in self.SUPPORTED_IMAGES:
            if image in from_line:
                self.inform_if_change_image(image, log_prefix)
                return self.is_valid_tag_for_image_name(from_line, image)
        return True

    def get_change_image_message(self, image, log_prefix):
        result = None
        if str(image) == "kth-nodejs-web":
            result = "*{}* Please change to `FROM kthse/kth-nodejs:sem_ver`. Image _kth-nodejs-web_ is depricated. Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(log_prefix)

        if str(image) == "kth-nodejs-api":
            result = "*{}* Please change to `FROM kthse/kth-nodejs:sem_ver`. Image _kth-nodejs-api_ is depricated. Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(log_prefix)

        return result

    def inform_if_change_image(self, image, log_prefix):
        message = self.get_change_image_message(image, log_prefix)
        
        if message:
            self.log.warn(message)
            Slack.on_warning(message)


    def is_valid_tag_for_image_name(self, from_line, image):
        
        # If array is empty, allow no tags for that image name.
        if not self.SUPPORTED_IMAGES[image]:
            return False

        # Allow all versions
        if self.SUPPORTED_IMAGES[image][0] == "*":
            return True

        for tag in self.SUPPORTED_IMAGES[image]:
            tag_pattern = ":{}".format(tag) # Match docker.io/redis":2.3
            if tag_pattern in from_line:
                return True
        return False

    def get_from_line(self):
        with open(self.get_docker_file_path()) as dockerfile:
            for line in dockerfile:
                if "FROM" in line:
                    return line.strip()

    def get_docker_file_path(self):
        stripped_root = Environment.get_project_root().rstrip('/')
        return '{}/Dockerfile'.format(stripped_root)
