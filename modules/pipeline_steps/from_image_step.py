__author__ = 'tinglev'

import logging
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.util import environment
from modules.util import slack
from modules.util import file_util
from modules.util import image_version_util


class FromImageStep(AbstractPipelineStep):

    
    
    IMAGE_RULES = {
        #
        #  Tags starting with the following are considered
        # to be safe to use.
        #
        # i.e: kthse/kth-os:3.8.0
        # "kth-os": [ "2.8" ] -> False
        # "kth-os": [ "3.8" ] -> False
        # "kth-os": [ "3.8.0" ] -> True
        # "kth-os": [ "3.8.0_abcdef" ] -> True
        #
        "kth-os": [ "3.9", "3.10" ],
        "kth-nodejs": [ "8.11", "9.11", "10.14"],
        "kth-play1": [ "1.5" ],
        "kth-play2": [ "2.2" ],
        "kth-python": [ "3.6", "3.7" ],

        #
        #  Allow all tags for an image.
        #  "openjdk": ["*"]
        #
        "redis": ["*"],
        "openjdk": ["*"],

        #
        # Disallow all tags for a image.
        #
        "kth-java": [ ],
        "oracle": [ ],
        "kth-nodejs-web": [ ],
        "kth-nodejs-api": [ ]
    }

    def __init__(self, image_rules=None):
        self.log = logging.getLogger(self.get_step_name())
        if image_rules:
            self.IMAGE_RULES = image_rules

    def get_required_env_variables(self): # pragma: no cover
        return [environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):
        from_line = self.get_from_line()
        if self.validate(from_line, data):
            self.log.debug("'FROM:' statement '{}' in Dockerfile is valid.".format(from_line))
        else:
            message = "*{}*: Dockerfile uses an unsupported and possibly unsecure `{}` image, please upgrade! See https://hub.docker.com/r/kthse/ for :docker: images.".format(image_version_util.get_image(data), from_line)
            self.log.warn(message)
            slack.on_warning(message)
        
        return data

    def validate(self, from_line, data):
        for image_name in self.IMAGE_RULES:
            if image_name in from_line:
                self.inform_if_change_image(image_name, data)
                return self.is_valid_tag_for_image_name(from_line, image_name)
        return True

    @staticmethod
    def get_change_image_message(image_name, data):

        if str(image_name) == "kth-nodejs-web":
            return ("*{}*: Please change to `FROM kthse/kth-nodejs:sem_ver`. "
                    "Image _kth-nodejs-web_ is depricated. "
                    "Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(
                        image_version_util.get_image(data)))

        if str(image_name) == "kth-nodejs-api":
            return ("*{}*: Please change to `FROM kthse/kth-nodejs:sem_ver`. "
                    "Image _kth-nodejs-api_ is depricated. "
                    "Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(
                        image_version_util.get_image(data)))

        return None

    def inform_if_change_image(self, image_name, data):

        message = self.get_change_image_message(image_name, data)
        
        if message:
            self.log.warn(message)
            slack.on_warning(message)

    def is_valid_tag_for_image_name(self, from_line, image_name):
        
        # If array is empty, allow no tags for that image name.
        if not self.IMAGE_RULES[image_name]:
            return False

        # Allow all versions
        if self.IMAGE_RULES[image_name][0] == "*":
            return True

        for tag in self.IMAGE_RULES[image_name]:
            tag_pattern = ":{}".format(tag) # ex: docker.io/redis":2.3"
            if tag_pattern in from_line:
                return True
        return False

    @staticmethod
    def get_from_line():
        rows = file_util.get_lines(DockerFileStep.FILE_DOCKERFILE)
        for row in rows:
            if "FROM " in row.upper():
                return row
        return None