__author__ = 'tinglev'

import logging
import sys
from modules.pipeline_steps.setup_step import SetupStep
from modules.pipeline_steps.docker_conf_step import DockerConfPipelineStep
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.pipeline_steps.build_local_step import BuildLocalStep
from modules.pipeline_steps.build_environment_to_file_step import BuildEnvironmentToFileStep
from modules.pipeline_steps.dry_run_step import DryRunStep
from modules.pipeline_steps.test_image_step import TestImageStep
from modules.pipeline_steps.tag_image_step import TagImageStep
from modules.pipeline_steps.push_image_step import PushImageStep
from modules.pipeline_steps.push_public_image_step import PushPublicImageStep
from modules.pipeline_steps.repo_supervisor_step import RepoSupervisorStep
from modules.pipeline_steps.unit_test_step import UnitTestStep
from modules.pipeline_steps.integration_test_step import IntegrationTestStep
from modules.pipeline_steps.from_image_step import FromImageStep
from modules.util.exceptions import PipelineException
from modules.util.slack import Slack
from modules.util.environment import Environment


class DockerDeployPipeline(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)

        # Configure pipeline
        self.first_step = SetupStep()
        # Check the content of docker.conf
        next_step = self.first_step.set_next_step(DockerConfPipelineStep())
        # Build new image version major.minor.path_githash
        next_step = next_step.set_next_step(ImageVersionStep())
        # Check Dockerfile exists
        next_step = next_step.set_next_step(DockerFileStep())
        # Check Dockerfiles FROM statement
        next_step = next_step.set_next_step(FromImageStep())
        # Write information about the current build to a json-file.
        next_step = next_step.set_next_step(BuildEnvironmentToFileStep())
        if Environment.get_experimental():
            next_step = next_step.set_next_step(RepoSupervisorStep())
        # Build the image to local registry
        next_step = next_step.set_next_step(BuildLocalStep())
        # Test run the image
        if Environment.use_dry_run():
            next_step = next_step.set_next_step(DryRunStep())
        # Run unit tests
        next_step = next_step.set_next_step(UnitTestStep())
        # Run integration tests
        next_step = next_step.set_next_step(IntegrationTestStep())
        # Do something (leftover?)
        next_step = next_step.set_next_step(TestImageStep())
        # Tag the buildt image with image version.
        next_step = next_step.set_next_step(TagImageStep())
        # Puch the tagged image to a repository.
        if Environment.get_push_public():
            next_step = next_step.set_next_step(PushPublicImageStep())
        else:
            next_step = next_step.set_next_step(PushImageStep())

    def run_pipeline(self):
        self.verify_environment()
        self.run_steps()

    def run_steps(self):
        try:
            self.log.info('Running Docker build pipeline')
            data = self.first_step.run_pipeline_step({})
        except PipelineException as p_ex:
            self.log.fatal('%s'.encode('UTF-8'), p_ex, exc_info=False)
            Slack.send_to_slack('<!channel> {}'.format(p_ex.slack_message))
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
