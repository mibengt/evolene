__author__ = 'tinglev'

import time
from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import pipeline_data, docker, environment

class DryRunStep(AbstractPipelineStep):

    def __init__(self):
        super(DryRunStep, self).__init__()
        self.timeout = 60
        self.sleep = 5

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [pipeline_data.LOCAL_IMAGE_ID]

    def run_step(self, data):
        if environment.use_dry_run():
            container_id = self.start_container(data)
            try:
                container_status = self.wait_for_container_created(container_id)
                if not self.is_running(container_status):
                    self.handle_step_error(
                        '<!channel> Failed to test run the newly built container on Jenkins. To disable test set Evolene env `SKIP_DRY_RUN="True"`'
                    )
            finally:
                self.stop_container(container_id)
            self.log.info(
                'Dry run of image with id "%s" successful',
                data[pipeline_data.LOCAL_IMAGE_ID]
            )
        return data

    def get_container_status(self, container_id): #pragma: no cover
        return docker.get_container_status(container_id)

    def start_container(self, data): #pragma: no cover
        return docker.run(data[pipeline_data.LOCAL_IMAGE_ID])

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
        docker.stop_and_remove_container(container_id)
