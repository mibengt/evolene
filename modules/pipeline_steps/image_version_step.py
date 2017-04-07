__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return [Environment.BUILD_NUMBER, Environment.GIT_COMMIT]

    def get_required_data_keys(self):
        return [Environment.IMAGE_VERSION]

    def _create_image_version(self, image_version):
        # 2.2, 2.3.0
        nr_punctuations = image_version.count('.')
        if nr_punctuations != 1:
            self._handle_step_error('docker.conf IMAGE_VERSION is "{}", should be "Major.Minor"'
                                    .format(image_version))
        build_number = os.environ[Environment.BUILD_NUMBER]
        commit_hash = os.environ[Environment.GIT_COMMIT]
        if len(commit_hash) > 7:
            commit_hash = commit_hash[:7]
        return self._format_image_version(image_version, build_number, commit_hash)

    def _format_image_version(self, image_version, build_number, commit_hash):
        return '{}.{}_{}'.format(image_version, build_number, commit_hash)

    def run_step(self, data):
        image_version = data[Environment.IMAGE_VERSION]
        final_image_version = self._create_image_version(image_version)
        data[Environment.IMAGE_VERSION] = final_image_version
        return data
