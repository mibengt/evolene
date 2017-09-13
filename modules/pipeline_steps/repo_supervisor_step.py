__author__ = 'tinglev@kth.se'

# docker pull kthse/repo-supervisor

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.docker import Docker
from modules.util.process import Process

class RepoSupervisorStep(AbstractPipelineStep):

    IMAGE_NAME = 'kthse/repo-supervisor'

    def get_required_env_variables(self): #pragma: no cover
        return []

    def get_required_data_keys(self): #pragma: no cover
        return []

    def run_step(self, data):
        image_name = RepoSupervisorStep.IMAGE_NAME
        image_grep_output = Docker.grep_image_id(image_name)
        if image_name not in image_grep_output:
            Docker.pull(image_name)
        result = self._run_supervisor()
        print result
        return data

    def _run_supervisor(self):
        cmd = ('docker run -it --rm -v ${WORKSPACE}:/opt/scan_me repo-supervisor '
               '/bin/bash -c "source ~/.bashrc && '
               'JSON_OUTPUT=1 node /opt/repo-supervisor/dist/cli.js /opt/scan_me"')
        return Process.run_with_output(cmd)
