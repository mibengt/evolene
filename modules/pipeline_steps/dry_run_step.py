__author__ = 'tinglev'

import time
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data
from modules.util.process import Process

class DryRunStep(AbstractPipelineStep):

    def __init__(self):
        super(DryRunStep, self).__init__()
        self.timeout = 60
        self.sleep = 5

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [Data.LOCAL_IMAGE_ID]

    def _get_container_status(self, container_id):
        status = Process.run_with_output('docker inspect --format=\'{{{{.State.Status}}}}\' {}'
                                         .format(container_id))
        return status.rstrip()

    def _start_container(self, data):
        container_id = Process.run_with_output('docker run -d {}'
                                               .format(data[Data.LOCAL_IMAGE_ID]))
        return container_id.rstrip()

    def _wait_for_container_created(self, container_id):
        container_status = self._get_container_status(container_id)
        wait_remaining = self.timeout
        while self._is_creating(container_status) and wait_remaining > 0:
            self.log.debug('Container is creating. Waiting for status change..')
            time.sleep(self.sleep)
            wait_remaining -= self.sleep
            container_status = self._get_container_status(container_id)
        return container_status

    def _is_running(self, container_status):
        # created|restarting|running|removing|paused|exited|dead
        return container_status == 'running'

    def _is_creating(self, container_status):
        # created|restarting|running|removing|paused|exited|dead
        return container_status == 'created'

    def _stop_container(self, container_id):
        Process.run_with_output('docker rm -f {}'.format(container_id))

    def run_step(self, data):
        container_id = self._start_container(data)
        try:
            container_status = self._wait_for_container_created(container_id)
            if not self._is_running(container_status):
                self._handle_step_error('Status of container after dry run is "{}"'
                                        .format(container_status))
        finally:
            self._stop_container(container_id)
        return data
