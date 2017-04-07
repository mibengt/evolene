__author__ = 'tinglev'

from abstract_pipeline_step import AbstractPipelineStep

class DockerConfPipelineStep(AbstractPipelineStep):

    def run_step(self, data):
        data['counter'] = data['counter'] + 1
        print 'Handled: {}'.format(data)
        return data

