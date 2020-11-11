__author__ = 'tinglev'

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util import image_version_util
from modules.util import pipeline_data
import re

class ImageVersionStep(AbstractPipelineStep):

    def get_required_env_variables(self): # pragma: no cover
        return [environment.BUILD_NUMBER, environment.GIT_COMMIT]

    def get_required_data_keys(self): # pragma: no cover
        return [pipeline_data.IMAGE_VERSION]

    def run_step(self, data): # pragma: no cover
        data[pipeline_data.SEM_VER] = self.get_sem_ver(data[pipeline_data.IMAGE_VERSION],
                                                       self.get_patch_version(data))
        data[pipeline_data.COMMIT_HASH] = environment.get_git_commit_clamped()
        data[pipeline_data.IMAGE_VERSION] = self.append_commit_hash(data[pipeline_data.SEM_VER])
        return data

    def get_patch_version(self, data):
        if pipeline_data.PATCH_VERSION in data:
            return data[pipeline_data.PATCH_VERSION]
        return environment.get_build_number()

    def get_sem_ver(self, image_version, patch_version):

        if not image_version_util.is_major_minor_only(image_version):
            self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor"'
                                   .format(image_version))
        return "{}.{}".format(image_version, patch_version)
        
        # if not image_version_util.is_major_minor_only(image_version):
        #     self.handle_step_error('IMAGE_VERSION in docker.conf is `{}`, must be "Major.Minor"'
        #                            .format(image_version))
        # branch_name = environment.get_git_branch()
        # if not branch_name in ('master', 'main'):
        #     return "{}-{}.{}".format(slugify(branch_name), image_version, patch_version)
        # else:
        #     return "{}.{}".format(image_version, patch_version)

    def append_commit_hash(self, sem_ver):
        return '{}_{}'.format(sem_ver, environment.get_git_commit_clamped())

    def get_commit_hash_clamped(self, length=7):
        commit_hash = environment.get_git_commit()
        if len(str(commit_hash)) > length:
            commit_hash = commit_hash[:length]
        return commit_hash

def slugify(name):
    """Take some name (any string) and return a version-slug-safe variant of it."""
    # This could be done better with an external dependency,
    # but branch-names are probably ascii anyway.
    # "feature/slånbärsöl" will become "feature.sl.nb.rs.l", so it errs on the safe side.
    # If the result is an empty string, substitute "unknown"
    return re.sub('[^a-z0-9]+', '.', name.lower()).strip('.') or 'unknown'
