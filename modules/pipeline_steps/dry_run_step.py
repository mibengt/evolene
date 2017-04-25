__author__ = 'tinglev'

import time
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util.data import Data
from modules.util.docker import Docker

class DryRunStep(AbstractPipelineStep):

    def __init__(self):
        super(DryRunStep, self).__init__()
        self.timeout = 60
        self.sleep = 5

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [Data.LOCAL_IMAGE_ID]

    def get_container_status(self, container_id): #pragma: no cover
        return Docker.get_container_status(container_id)

    def start_container(self, data): #pragma: no cover
        return Docker.run(data[Data.LOCAL_IMAGE_ID])

    def wait_for_container_created(self, container_id):
        container_status = self.get_container_status(container_id)
        wait_remaining = self.timeout
        while self.is_creating(container_status) and wait_remaining > 0:
            self.log.debug('Container is creating. Waiting for status change..')
            time.sleep(self.sleep)
            wait_remaining -= self.sleep
            container_status = self.get_container_status(container_id)
        return container_status

    def is_running(self, container_status):
        # created|restarting|running|removing|paused|exited|dead
        return container_status == 'running'

    def is_creating(self, container_status):
        # created|restarting|running|removing|paused|exited|dead
        return container_status == 'created'

    def stop_container(self, container_id): #pragma: no cover
        Docker.stop_and_remove_container(container_id)

    def run_step(self, data):
        container_id = self.start_container(data)
        try:
            container_status = self.wait_for_container_created(container_id)
            if not self.is_running(container_status):
                self.handle_step_error('Status of container after dry run is "{}"'
                                       .format(container_status))
        finally:
            self.stop_container(container_id)
        self.log.info('Dry run of image with id "%s" successful', data[Data.LOCAL_IMAGE_ID])
        return data
