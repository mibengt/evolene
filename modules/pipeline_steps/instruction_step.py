__author__ = 'tinglev'

import logging
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.util.environment import Environment
from modules.util.slack import Slack
from modules.util.file_util import FileUtil
from modules.util.image_version_util import ImageVersionUtil


class InstructionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): # pragma: no cover
        return []

    def run_step(self, data):

        for instruction in FileUtil.get_lines(DockerFileStep.FILE_DOCKERFILE):
            if self.is_instrucation_entrypoint(instruction):
                message = self.get_change_message(instruction, data)
                self.log.warn(message)
                Slack.on_warning(message)        
        return data        

    def is_instrucation_entrypoint(self, instruction):
        if str(instruction).startswith("ENTRYPOINT"):
            return True
        return False

    def get_change_message(self, instruction, data):
        return "*{}*: Please change {}  to `{}`.".format(
            ImageVersionUtil.get_image(data),
            instruction,
            self.get_change_to_instruction(instruction))

    def get_change_to_instruction(self, instruction):
        return str(instruction).replace('ENTRYPOINT', 'CMD')