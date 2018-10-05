__author__ = 'tinglev'

import re
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util.image_version_util import ImageVersionUtil

from modules.util.data import Data

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.BUILD_NUMBER, Environment.GIT_COMMIT]

    def get_required_data_keys(self): # pragma: no cover
        return [Data.IMAGE_VERSION]

    def run_step(self, data): # pragma: no cover
        data[Data.SEM_VER] = self.get_semver(data[Data.IMAGE_VERSION], data[Data.PATCH_VERSION])
        data[Data.COMMIT_HASH]   = self.get_commit_hash_clamped()
        data[Data.IMAGE_VERSION] = self.append_commit_hash(data[Data.SEM_VER])
        return data

    def get_semver(self, image_version, patch_version):
        if not ImageVersionUtil.is_major_minor_only(image_version):
            self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor"'.format(image_version))

        if not patch_version:
            patch_version = Environment.get_build_number()

        return "{}.{}".format(image_version, patch_version)

    def append_commit_hash(self, image_version):
        return '{}_{}'.format(image_version,  self.get_commit_hash_clamped())

    def get_commit_hash_clamped(self, length=7):
        commit_hash = Environment.get_git_commit()
        if len(commit_hash) > length:
            commit_hash = commit_hash[:length]
        return commit_hash

