__author__ = 'tinglev@kth.se'

import json
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.docker import Docker
from modules.util.process import Process
from modules.util.environment import Environment
from modules.util.exceptions import PipelineException

class RepoSupervisorStep(AbstractPipelineStep):

    IMAGE_NAME = 'kthse/repo-supervisor'
    EXCLUDED_DIRECTORIES = ['node_modules']

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
        result = self._run_supervisor(image_name)
        if result:
            result_json = json.loads(result)
            for filename, _ in result_json['result'].iteritems():
                for directory in RepoSupervisorStep.EXCLUDED_DIRECTORIES:
                    if directory not in filename:
                        self.log.info('Found suspicious string in file "%s"', filename)
        else:
            self.log.debug('Repo-supervisor found nothing')
        return data

    def _run_supervisor(self, image_name):
        cmd = ('docker run --rm -v ${{WORKSPACE}}:/opt/scan_me {} '
               '/bin/bash -c "source ~/.bashrc && '
               'JSON_OUTPUT=1 node /opt/repo-supervisor/dist/cli.js /opt/scan_me"'
               .format(image_name))
        try:
            return Process.run_with_output(cmd)
        except PipelineException as pipeline_ex:
            # Special handling while waiting for https://github.com/auth0/repo-supervisor/pull/5
            if 'Not detected any secrets in files' in pipeline_ex.message:
                return None
            raise
