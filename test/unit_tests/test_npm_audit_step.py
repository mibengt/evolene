__author__ = 'tinglev'

import json
import os
import sys
import unittest
from unittest import mock
from modules.pipeline_steps.npm_audit_step import NpmAuditStep
from modules.util import pipeline_data

class NpmAuditStepTests(unittest.TestCase):

    def test_approve_audit(self):
        sys.exit = mock.MagicMock()
        current_path = os.path.dirname(os.path.abspath(__file__))
        audit_json = json.loads(
            open(os.path.join(current_path, '../data/npm/audit.json')).read()
        )
        data = {pipeline_data.NPM_CONF_ALLOW_CRITICALS: 1}
        step = NpmAuditStep()
        data = step.approve_audit(data, audit_json)
        sys.exit.assert_not_called()
        sys.exit.reset_mock()
        self.assertFalse(pipeline_data.IGNORED_CRITICALS in data)
        audit_json['metadata']['vulnerabilities']['critical'] = 1
        data = step.approve_audit(data, audit_json)
        self.assertEqual(data[pipeline_data.IGNORED_CRITICALS], 1)
        sys.exit.assert_not_called()
        sys.exit.reset_mock()
        step.approve_audit({}, audit_json)
        sys.exit.assert_called_once()
