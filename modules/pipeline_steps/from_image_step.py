__author__ = 'tinglev'

import logging
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.util.environment import Environment
from modules.util.slack import Slack
from modules.util.file_util import FileUtil
from modules.util.image_version_util import ImageVersionUtil


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
        if self.validate(from_line):
            self.log.debug("'FROM:' statement '{}' in Dockerfile is valid.".format(from_line))
        else:
            message = "*{}*: Dockerfile uses an unsupported and possibly unsecure `{}` image, please upgrade!".format(log_prefix, from_line)
            self.log.warn(message)
            Slack.on_warning(message)
        
        return data

    def validate(self, from_line, data):
        for image_name in self.IMAGE_RULES:
            if image_name in from_line:
                self.inform_if_change_image(image_name, data)
                return self.is_valid_tag_for_image_name(from_line, image_name)
        return True

    def get_change_image_message(self, image_name, data):

        if str(image_name) == "kth-nodejs-web":
            return ("*{}*: Please change to `FROM kthse/kth-nodejs:sem_ver`. "
                    "Image _kth-nodejs-web_ is depricated. "
                    "Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(
                        ImageVersionUtil.get_image(data)))

        if str(image_name) == "kth-nodejs-api":
            return ("*{}*: Please change to `FROM kthse/kth-nodejs:sem_ver`. "
                    "Image _kth-nodejs-api_ is depricated. "
                    "Info: https://gita.sys.kth.se/Infosys/kth-nodejs".format(
                        ImageVersionUtil.get_image(data)))

        return None

    def inform_if_change_image(self, image_name, data):

        message = self.get_change_image_message(image_name, data)
        
        if message:
            self.log.warn(message)
            Slack.on_warning(message)

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

    def get_from_line(self):
        rows = FileUtil.get_lines(DockerFileStep.FILE_DOCKERFILE)
        for row in rows:
            if "FROM" in row:
                return row