__author__ = 'tinglev'

import os
import unittest
from modules.util.environment import Environment
from modules.util.docker import Docker
from modules.util.process import Process
from modules.util.exceptions import PipelineException


class DockerTests(unittest.TestCase):

    IMAGE_ID = None
    CONTAINER_ID = None

    @classmethod
    def tearDownClass(cls):
        Process.run_with_output('docker rm -f {}'.format(DockerTests.CONTAINER_ID))
        Process.run_with_output('docker rmi -f {}'.format(DockerTests.IMAGE_ID))

    def test_all(self):
        self._test_build()
        self._test_tag_image()
        self._test_run()
        self._test_get_container_status()
        self._test_grep_image_id()
        self._test_stop_and_rm_container()

    def _test_build(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        result = Docker.build()
        DockerTests.IMAGE_ID = result.replace('sha256:', '')[:12]
        self.assertIn('sha256:', result)

    def _test_tag_image(self):
        Docker.tag_image(DockerTests.IMAGE_ID, 'test_tag')

    def _test_run(self):
        container_id = Docker.run(DockerTests.IMAGE_ID)
        DockerTests.CONTAINER_ID = container_id
        self.assertEqual(len(container_id), 64)

    def _test_get_container_status(self):
        status = Docker.get_container_status(DockerTests.CONTAINER_ID)
        self.assertEqual(status, 'running')

    def _test_grep_image_id(self):
        grep_return = Docker.grep_image_id(DockerTests.IMAGE_ID)
        self.assertTrue(DockerTests.IMAGE_ID in grep_return)
        # Test that the tag from the earlier step also appears here
        self.assertTrue('test_tag' in grep_return)

    def _test_stop_and_rm_container(self):
        Docker.stop_and_remove_container(DockerTests.CONTAINER_ID)
        self.assertRaises(PipelineException, Docker.get_container_status, DockerTests.CONTAINER_ID)
