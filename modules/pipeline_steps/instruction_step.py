__author__ = 'tinglev'

import logging
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.util.environment import Environment
from modules.util.slack import Slack
from modules.util import file_util
from modules.util import pipeline_data
from modules.util import image_version_util


class InstructionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return [pipeline_data.IMAGE_NAME, pipeline_data.IMAGE_VERSION]

    def run_step(self, data):
        for instruction in file_util.get_lines(DockerFileStep.FILE_DOCKERFILE):
            if self.is_instruction_entrypoint(instruction):
                message = self.get_change_message(instruction, data)
                self.log.warning(message)
                Slack.on_warning(message)
        return data

    def is_instruction_entrypoint(self, instruction):
        if str(instruction).startswith("ENTRYPOINT"):
            return True
        return False

    def get_change_message(self, instruction, data):
        return "*{}*: In `/Dockerfile` change `{}` to: ```{}```".format(
            image_version_util.get_image(data),
            instruction,
            self.get_change_to_instruction(instruction))

    def get_change_to_instruction(self, instruction):
        return str(instruction).replace('ENTRYPOINT', 'CMD')
