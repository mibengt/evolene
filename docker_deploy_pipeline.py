__author__ = 'tinglev'

import fire
from docker_conf_step import DockerConfPipelineStep

class DockerDeployPipeline(object):

    def __init__(self):
        self.dcp1 = DockerConfPipelineStep()
        self.dcp2 = DockerConfPipelineStep()
        self.dcp1.set_successor(self.dcp2)

    def run_pipeline(self):
        self.dcp1.run_pipeline({'counter': 0})

if(__name__) == '__main__':
    fire.Fire(DockerDeployPipeline)
        