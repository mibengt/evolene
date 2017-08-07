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
from modules.util.exceptions import PipelineException
from modules.util.slack import Slack


class DockerDeployPipeline(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)

        # Create pipeline steps
        self.setup_step = SetupStep()
        self.conf_step = DockerConfPipelineStep()
        self.image_version_step = ImageVersionStep()
        self.docker_file_step = DockerFileStep()
        self.build_local_step = BuildLocalStep()
        self.dry_run_step = DryRunStep()
        self.test_image_step = TestImageStep()
        self.tag_image_step = TagImageStep()
        self.push_image_step = PushImageStep()

        # Configure pipeline
        self.first_step = self.setup_step
        self.first_step \
            .set_next_step(self.conf_step) \
            .set_next_step(self.image_version_step) \
            .set_next_step(self.docker_file_step) \
            .set_next_step(self.build_local_step) \
            .set_next_step(self.dry_run_step) \
            .set_next_step(self.test_image_step) \
            .set_next_step(self.tag_image_step) \
            .set_next_step(self.push_image_step)

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
