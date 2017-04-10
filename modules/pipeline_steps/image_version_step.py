__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.data import Data

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.BUILD_NUMBER, Environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return [Environment.IMAGE_VERSION]

    def _create_image_version(self, image_version):
        self._check_image_version(image_version)
        build_number = Environment.get_build_number()
        commit_hash = self._get_clamped_commit_hash()
        return self._format_image_version(image_version, build_number, commit_hash)

    def _check_image_version(self, image_version):
        match = re.match(r'^[0-9]+\.[0-9]$', image_version)
        if not match:
            self._handle_step_error('docker.conf IMAGE_VERSION is "{}", should be "Major.Minor"'
                                    .format(image_version))

    def _get_clamped_commit_hash(self, length=7):
        commit_hash = Environment.get_git_commit()
        if len(commit_hash) > length:
            commit_hash = commit_hash[:length]
        return commit_hash

    def _format_image_version(self, image_version, build_number, commit_hash):
        return '{}.{}_{}'.format(image_version, build_number, commit_hash)

    def run_step(self, data):
        image_version = data[Environment.IMAGE_VERSION]
        final_image_version = self._create_image_version(image_version)
        data[Data.IMAGE_VERSION] = final_image_version
        return data
