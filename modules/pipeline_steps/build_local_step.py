__author__ = 'tinglev'

import os
import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.process import Process
from modules.util.environment import Environment
from modules.util.data import Data
from modules.util.docker import Docker

class BuildLocalStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self):
        return []

    def run_step(self, data):
        image_id = self.run_build()
        image_grep_output = self.verify_built_image(image_id)
        size = self.get_image_size(image_grep_output)
        data[Data.IMAGE_SIZE] = size
        data[Data.LOCAL_IMAGE_ID] = image_id
        self.log.info('Built image with id "%s" and size "%s"', image_id, size)
        return data

    def format_image_id(self, image_id):
        self.log.debug('Full image id is "%s"', image_id)
        image_id = image_id.replace('sha256:', '')
        return image_id[:12]

    def verify_built_image(self, image_id):
        image_grep_output = Docker.grep_image_id(image_id)
        self.log.debug('Grep for image id returned "%s"', image_grep_output.rstrip())
        if not image_id in image_grep_output:
            self.handle_step_error('Could not find locally built image')
        return image_grep_output

    def get_image_size(self, image_grep_output):
        size = re.search(r'[0-9]+ MB', image_grep_output)
        if size:
            return size.group(0)
        return 'N/A'

    def run_build(self):
        image_id = Docker.build()
        return self.format_image_id(image_id)



