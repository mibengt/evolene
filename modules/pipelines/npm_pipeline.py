__author__ = 'tinglev'

import logging
import sys
from modules.pipeline_steps.setup_step import SetupStep
from modules.pipeline_steps.read_conf_step import ReadConfFileStep
from modules.pipeline_steps.npm_build_step import NpmBuildStep
from modules.pipeline_steps.npm_login_step import NpmLoginStep
from modules.pipeline_steps.load_package_json_step import LoadPackageJsonStep
from modules.pipeline_steps.npm_version_step import NpmVersionStep
from modules.pipeline_steps.npm_package_name_step import NpmPackageNameStep
from modules.pipeline_steps.npm_version_changed_step import NpmVersionChangedStep
from modules.util.exceptions import PipelineException
from modules.util.print_util import PrintUtil
from modules.util.slack import Slack
from modules.util import pipeline

class NpmPipeline(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)
        # Configure pipeline
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            SetupStep(),
            LoadPackageJsonStep(),
            ReadConfFileStep('npm.conf'),
            NpmVersionStep(),
            NpmPackageNameStep(),
            NpmVersionChangedStep(),
            NpmLoginStep(),
            NpmBuildStep()
        ])

    def run_pipeline(self):
        self.verify_environment()
        self.run_steps()

    def run_steps(self):
        try:
            self.log.info('Running npm pipeline')
            data = self.pipeline_steps[0].run_pipeline_step({})
        except PipelineException as p_ex:
            self.log.fatal('%s'.encode('UTF-8'), p_ex, exc_info=False)
            Slack.send_to_slack('<!channel> {}'.format(p_ex.slack_message))
            PrintUtil.red("Such bad, very learning")
            sys.exit(1)
        else:
            self.log.info('Pipeline done. Pipeline data: %s', data)

    def verify_environment(self):
        try:
            self.log.info('Running environment verification')
            step = self.pipeline_steps[0]
            while step:
                step.step_environment_ok()
                step = step.next_step
        except PipelineException as p_ex:
            self.log.fatal('Caught exception: %s', p_ex, exc_info=True)
