__author__ = 'tinglev'

import logging
import sys
from modules.pipeline_steps.setup_step import SetupStep
from modules.pipeline_steps.docker_conf_step import DockerConfPipelineStep
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.pipeline_steps.build_local_step import BuildLocalStep
from modules.pipeline_steps.dry_run_step import DryRunStep
from modules.pipeline_steps.test_image_step import TestImageStep
from modules.pipeline_steps.tag_image_step import TagImageStep
from modules.pipeline_steps.push_image_step import PushImageStep
from modules.pipeline_steps.repo_supervisor_step import RepoSupervisorStep
from modules.pipeline_steps.unit_test_step import UnitTestStep
from modules.pipeline_steps.unit_test_step import IntegrationTestStep
from modules.util.exceptions import PipelineException
from modules.util.slack import Slack
from modules.util.environment import Environment


class DockerDeployPipeline(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)

        # Configure pipeline
        self.first_step = SetupStep()
        next_step = self.first_step.set_next_step(DockerConfPipelineStep())
        next_step = next_step.set_next_step(ImageVersionStep())
        next_step = next_step.set_next_step(DockerFileStep())
        if Environment.get_experimental():
            next_step = next_step.set_next_step(RepoSupervisorStep())
        next_step = next_step.set_next_step(BuildLocalStep())
        next_step = next_step.set_next_step(DryRunStep())
        if Environment.get_experimental():
            next_step = next_step.set_next_step(UnitTestStep())
        if Environment.get_experimental():
            next_step = next_step.set_next_step(IntegrationTestStep()
        next_step = next_step.set_next_step(TestImageStep())
        next_step = next_step.set_next_step(TagImageStep())
        next_step = next_step.set_next_step(PushImageStep())

    def run_pipeline(self):
        self.verify_environment()
        self.run_steps()

    def run_steps(self):
        try:
            self.log.info('Running Docker build pipeline')
            data = self.first_step.run_pipeline_step({})
        except PipelineException as p_ex:
            self.log.fatal('Caught exception: %s', p_ex, exc_info=True)
            Slack.send_to_slack('Fatal exception in build pipeline: ```{}```'.format(p_ex))
            sys.exit(1)
        else:
            self.log.info('Build and push successful. Pipeline data: %s', data)
            Slack.on_successful_deploy(data)

    def verify_environment(self):
        try:
            self.log.info('Running environment verification')
            step = self.first_step
            while step:
                step.step_environment_ok()
                step = step.next_step
        except PipelineException as p_ex:
            self.log.fatal('Caught exception: %s', p_ex, exc_info=True)
