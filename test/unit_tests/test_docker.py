__author__ = 'tinglev'

import os
import unittest
from modules.util.environment import Environment
from modules.util.docker import Docker
from modules.util.process import Process
from modules.util.exceptions import PipelineException


class DockerTest(unittest.TestCase):

    IMAGE_ID = None
    CONTAINER_ID = None

    @classmethod
    def tearDownClass(cls):
        Process.run_with_output('docker rm -f {}'.format(DockerTest.CONTAINER_ID))
        Process.run_with_output('docker rmi -f {}'.format(DockerTest.IMAGE_ID))

    def test_0_build(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        result = Docker.build()
        self.assertIn('sha256:', result)
        DockerTest.IMAGE_ID = result.replace('sha256:', '')[:12]

    def test_1_run(self):
        container_id = Docker.run(DockerTest.IMAGE_ID)
        self.assertEqual(len(container_id), 65)
        DockerTest.CONTAINER_ID = container_id

    def test_2_get_container_status(self):
        status = Docker.get_container_status(DockerTest.CONTAINER_ID)
        self.assertEqual(status, 'running')

    def test_3_grep_image_id(self):
        grep_return = Docker.grep_image_id(DockerTest.IMAGE_ID)
        self.assertTrue(DockerTest.IMAGE_ID in grep_return)

    def test_4_stop_and_rm_container(self):
        Docker.stop_and_remove_container(DockerTest.CONTAINER_ID)
        self.assertRaises(PipelineException, Docker.get_container_status, DockerTest.CONTAINER_ID)
