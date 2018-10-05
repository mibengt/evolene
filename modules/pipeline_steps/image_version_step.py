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
        data[Data.SEM_VER] = self.get_sem_ver(data[Data.IMAGE_VERSION], self.get_patch_version(data))
        data[Data.COMMIT_HASH]   = self.get_commit_hash_clamped()
        data[Data.IMAGE_VERSION] = self.append_commit_hash(data[Data.SEM_VER])
        return data
    
    def get_patch_version(self, data):
        if Data.PATCH_VERSION in data:
            return data[Data.PATCH_VERSION]
        return Environment.get_build_number()

    def get_sem_ver(self, image_version, patch_version):
        if not ImageVersionUtil.is_major_minor_only(image_version):
            self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor"'.format(image_version))
        return "{}.{}".format(image_version, patch_version)

    def append_commit_hash(self, sem_ver):
        return '{}_{}'.format(sem_ver,  self.get_commit_hash_clamped())

    def get_commit_hash_clamped(self, length=7):
        commit_hash = Environment.get_git_commit()
        if len(commit_hash) > length:
            commit_hash = commit_hash[:length]
        return commit_hash

