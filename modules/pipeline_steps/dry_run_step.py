__author__ = 'tinglev'

import time
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data
from modules.util.process import Process

class DryRunStep(AbstractPipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [Data.LOCAL_IMAGE_ID]

    def _get_container_status(self, container_id):
        status = Process.run_with_output('docker inspect --format=\'{{{{.State.Status}}}}\' {}'
                                         .format(container_id))
        return status.rstrip()

    def _start_container(self, data):
        return Process.run_with_output('docker run -d {}'
                                       .format(data[Data.LOCAL_IMAGE_ID]))

    def run_step(self, data):
        container_id = self._start_container(data)
        container_status = self._get_container_status(container_id)
        # created|restarting|running|removing|paused|exited|dead
        timeout = 60
        while container_status == 'created' and timeout > 0:
            self.log.debug('Container is creating. Waiting for status change..')
            time.sleep(5)
            timeout -= 5
            container_status = self._get_container_status(container_id)
        if container_status != 'running':
            self._handle_step_error('Status of container after dry run is "{}"'.format(container_status))
        return data
