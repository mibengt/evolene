__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.slack import Slack
import logging

class FromImageStep(AbstractPipelineStep):

    
    IMAGE_RULES = {
        # Tags starting with.
        # 
        # i.e: kthse/kth-os:3.8.0
        # "kth-os": [ "3.8" ]
        # "kth-os": [ "3.8.0" ]
        # "kth-os": [ "3.8.0_abcdef" ]
        #
        "kth-os": [ "3.8" ],
        "kth-nodejs": [ "8.11", "9.11"],
        "kth-nodejs-web": [ "2.4" ],
        "kth-nodejs-api": [ "2.4" ],
        "kth-play1": [ "1.5" ],
        "kth-play2": [ "2.2" ],
        
        #
        #  Allow all tags
        #
        "redis": ["*"],

        #
        # Disallow all tags
        #
        "kth-python": [ ],
        "kth-java": [ ],
        "oracle": [ ],
    }

    def __init__(self, image_rules=None):
        self.log = logging.getLogger(self.get_step_name())
        if image_rules:
            self.IMAGE_RULES = image_rules

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        from_line = self.get_from_line()
        log_prefix = "{}:{}".format(data[Data.IMAGE_NAME], data[Data.IMAGE_VERSION])
        if self.validate(from_line, log_prefix):
            self.log.debug("'FROM:' statement '{}' in Dockerfile is valid.".format(from_line))
        else:
            message = "*{}*: Dockerfile uses an unsupported and possibly unsecure `{}` image, please upgrade!".format(log_prefix, from_line)
            self.log.warn(message)
            Slack.on_warning(message)
        
        return data

    def validate(self, from_line, log_prefix):
        for image in self.IMAGE_RULES:
            if image in from_line:
                self.inform_if_change_image(image, log_prefix)
                return self.is_valid_tag_for_image_name(from_line, image)
        return True

    def get_change_image_message(self, image, log_prefix):
        result = None
        if "kth-nodejs-web" in image:
            result = "*{}*: Please change to `FROM kthse/kth-nodejs:sem_ver`. Image _kth-nodejs-web_ is depricated. Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(log_prefix)

        if "kth-nodejs-api" in image:
            result = "*{}*: Please change to `FROM kthse/kth-nodejs:sem_ver`. Image _kth-nodejs-api_ is depricated. Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(log_prefix)

        return result

    def inform_if_change_image(self, image, log_prefix):
        message = self.get_change_image_message(image, log_prefix)
        
        if message:
            self.log.warn(message)
            Slack.on_warning(message)


    def is_valid_tag_for_image_name(self, from_line, image):
        
        # If array is empty, allow no tags for that image name.
        if not self.IMAGE_RULES[image]:
            return False

        # Allow all versions
        if self.IMAGE_RULES[image][0] == "*":
            return True

        for tag in self.IMAGE_RULES[image]:
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
