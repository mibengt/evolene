__author__ = 'tinglev'

from modules.pipeline_steps.docker_conf_step import DockerConfPipelineStep

class DockerDeployPipeline(object):

    def __init__(self):
        self.dcp1 = DockerConfPipelineStep()
        self.dcp2 = DockerConfPipelineStep()
        self.dcp1.set_successor(self.dcp2)

    def run_pipeline(self):
        self.dcp1.run_pipeline({'counter': 0})
        