__author__ = 'tinglev'

import os
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep

class ImageVersionStep(AbstractPipelineStep):

    GIT_COMMIT = 'GIT_COMMIT'
    BUILD_NUMBER = 'BUILD_NUMBER'
    IMAGE_VERSION = 'IMAGE_VERSION'

    def get_required_env_variables(self):
        return [ImageVersionStep.BUILD_NUMBER, ImageVersionStep.GIT_COMMIT]

    def get_required_data_keys(self):
        return [ImageVersionStep.IMAGE_VERSION]

    def _format_image_version(self, image_version):
        # 2.2, 2.3.0
        nr_punctuations = image_version.count('.')
        if nr_punctuations != 1:
            self._handle_step_error('docker.conf IMAGE_VERSION is "{}", should be "Major.Minor"'
                                    .format(image_version))
        build_number = os.environ[ImageVersionStep.BUILD_NUMBER]
        commit_hash = os.environ[ImageVersionStep.GIT_COMMIT]
        if len(commit_hash) > 7:
            commit_hash = commit_hash[:7]
        return '{}.{}_{}'.format(image_version, build_number, commit_hash)

    def run_step(self, data):
        image_version = data[ImageVersionStep.IMAGE_VERSION]
        final_image_version = self._format_image_version(image_version)
        data['FINAL_IMAGE_VERSION'] = final_image_version
        return data
