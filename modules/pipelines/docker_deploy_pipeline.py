__author__ = 'tinglev'

from modules.pipeline_steps.docker_conf_step import DockerConfPipelineStep
from modules.pipeline_steps.image_version_step import ImageVersionStep
from modules.pipeline_steps.docker_file_step import DockerFileStep
from modules.pipeline_steps.build_local_step import BuildLocalStep
from modules.pipeline_steps.dry_run_step import DryRunStep
from modules.pipeline_steps.test_image_step import TestImageStep
from modules.pipeline_steps.image_info_step import ImageInfoStep
from modules.pipeline_steps.push_image_step import PushImageStep


class DockerDeployPipeline(object):

    def __init__(self):
        # Create pipeline steps
        self.conf_step = DockerConfPipelineStep()
        self.image_version_step = ImageVersionStep()
        self.docker_file_step = DockerFileStep()
        self.build_local_step = BuildLocalStep()
        self.dry_run_step = DryRunStep()
        self.test_image_step = TestImageStep()
        self.image_info_step = ImageInfoStep()
        self.push_image_step = PushImageStep()

        # Configure pipeline
        self.first_step = self.conf_step
        self.first_step \
            .set_next_step(self.image_version_step) \
            .set_next_step(self.docker_file_step) \
            .set_next_step(self.build_local_step) \
            .set_next_step(self.dry_run_step) \
            .set_next_step(self.test_image_step) \
            .set_next_step(self.image_info_step) \
            .set_next_step(self.push_image_step)

    def run_pipeline(self):
        data = self.conf_step.run_pipeline_step({})
        print data
        