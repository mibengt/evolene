__author__ = 'tinglev'

import os
import unittest
from mock import patch
from modules.util.environment import Environment
from modules.pipeline_steps.from_image_step import FromImageStep

class DockerFileTests(unittest.TestCase):

    TEST_ALLOWED_IMAGES = {
        "kth-app": ["1.0", "2.0" ],
        "other-app": ["latest"],
        "oracle": [ ],
        "redis": ["*"]
    }

    def test_docker_file_exists(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        os.environ[Environment.PROJECT_ROOT] = os.path.join(current_path, '../data')
        fis = FromImageStep()
        result = fis.get_from_line()
        self.assertEquals("FROM redis", result)

    def test_supported_kth_image(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate("FROM kthreg/kth-app:1.0"))

    def test_not_supported_kth_image(self):
        self.assertFalse(FromImageStep(self.TEST_ALLOWED_IMAGES).validate("FROM kthreg/kth-app:0.0"))
    
    def test_other_app_image(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate("FROM docker.io/other-app:latest"))

    def test_allow_all_unknown_images(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate("FROM docker.io/someimage:latest"))

    def test_all_versions_invalid(self):
        self.assertFalse(FromImageStep(self.TEST_ALLOWED_IMAGES).validate("FROM docker.io/oracle:11.1"))

    def test_allow_all_versions(self):
        self.assertTrue(FromImageStep(self.TEST_ALLOWED_IMAGES).validate("FROM docker.io/redis:13.37"))
