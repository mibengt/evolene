__author__ = 'tinglev@kth.se'

# docker pull kthse/repo-supervisor

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.docker import Docker
from modules.util.process import Process
from modules.util.environment import Environment

class RepoSupervisorStep(AbstractPipelineStep):

    IMAGE_NAME = 'kthse/repo-supervisor'

    def get_required_env_variables(self): #pragma: no cover
        return [Environment.PROJECT_ROOT]

    def get_required_data_keys(self): #pragma: no cover
        return []

    def run_step(self, data):
        image_name = RepoSupervisorStep.IMAGE_NAME
        image_grep_output = Docker.grep_image_id(image_name)
        if image_name not in image_grep_output:
            self.log.debug('Couldnt find local image "%s". Pulling from docker.io.',
                           image_name)
            Docker.pull(image_name)
        self.log.debug('Running repo supervisor')
        result = self._run_supervisor()
        self.log.info('Repo-supervisor result was: "%s"', result)
        return data

    def _run_supervisor(self):
        cmd = ('docker run --rm -v ${WORKSPACE}:/opt/scan_me repo-supervisor '
               '/bin/bash -c "source ~/.bashrc && '
               'JSON_OUTPUT=1 node /opt/repo-supervisor/dist/cli.js /opt/scan_me"')
        return Process.run_with_output(cmd)
