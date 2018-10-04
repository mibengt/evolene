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

    def get_patch_version(self, image_version):
        return Environment.get_build_number()

    def _create_image_version(self, image_version): # pragma: no cover
        self.check_image_version(image_version)
        commit_hash = self.get_clamped_commit_hash()
        return self.format_semver_version(image_version, commit_hash, Environment.get_build_number())

    def check_image_version(self, image_version):
        if not ImageVersionUtil.is_valid(image_version):
            if ImageVersionUtil.use_patch_from_docker_conf():
                self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor"'.format(image_version))
            else:
                self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor.Patch" since BUILD_NUMBER="docker.conf" is used.'.format(image_version))

    def get_clamped_commit_hash(self, length=7):
        commit_hash = Environment.get_git_commit()
        if len(commit_hash) > length:
            commit_hash = commit_hash[:length]
        return commit_hash

    def get_semver_version(self, image_version, build_number):

        if image_version.count('.') > 2:
            raise ValueError("'{}' is not in major.minor or major.minor.patch format.".format(image_version))

        # image_version is "1.2.3" (major.minor.patch)
        if image_version.count('.') is 2:
            return image_version # "1.2.3"

        # image_version is "1.2" (major.minor only) add build number as patch version.
        return '{}.{}'.format(image_version, build_number)

    def format_semver_version(self, image_version, commit_hash, build_number):
        return '{}_{}'.format(self.get_semver_version(image_version, build_number), commit_hash)

    def run_step(self, data): # pragma: no cover
        image_version = data[Data.IMAGE_VERSION]
        final_image_version = self._create_image_version(image_version)
        data[Data.SEM_VER] = self.get_semver_version(image_version, Environment.get_build_number())
        data[Data.IMAGE_VERSION] = final_image_version
        data[Data.COMMIT_HASH] = self.get_clamped_commit_hash()
        return data
