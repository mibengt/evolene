__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.environment import Environment
from modules.util import image_version_util
from modules.util import pipeline_data

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [Environment.BUILD_NUMBER, Environment.GIT_COMMIT]

    def get_required_data_keys(self): # pragma: no cover
        return [pipeline_data.IMAGE_VERSION]

    def run_step(self, data): # pragma: no cover
        data[pipeline_data.SEM_VER] = self.get_sem_ver(data[pipeline_data.IMAGE_VERSION], self.get_patch_version(data))
        data[pipeline_data.COMMIT_HASH]   = self.get_commit_hash_clamped()
        data[pipeline_data.IMAGE_VERSION] = self.append_commit_hash(data[pipeline_data.SEM_VER])
        return data
    
    def get_patch_version(self, data):
        if pipeline_data.PATCH_VERSION in data:
            return data[pipeline_data.PATCH_VERSION]
        return Environment.get_build_number()

    def get_sem_ver(self, image_version, patch_version):
        if not image_version_util.is_major_minor_only(image_version):
            self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor"'.format(image_version))
        return "{}.{}".format(image_version, patch_version)

    def append_commit_hash(self, sem_ver):
        return '{}_{}'.format(sem_ver, self.get_commit_hash_clamped())

    def get_commit_hash_clamped(self, length=7):
        commit_hash = Environment.get_git_commit()
        if len(commit_hash) > length:
            commit_hash = commit_hash[:length]
        return commit_hash

