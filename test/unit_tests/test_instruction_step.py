__author__ = 'tinglev'

import os
import unittest
from modules.util.environment import Environment
from modules.pipeline_steps.instruction_step import InstructionStep
from modules.util.data import Data

class InstructionStepTests(unittest.TestCase):

    def is_instrucation_entrypoint(self):
        self.assertTrue(InstructionStep().is_instrucation_entrypoint('ENTRYPOINT ["make", "main.cpp]'))

    def is_instrucation_cmd(self):
        self.assertFalse(InstructionStep().is_instrucation_entrypoint('CMD ["make", "main.cpp]'))

    def is_instrucation_message_on_change(self):
        message = InstructionStep().get_change_message('ENTRYPOINT ["make", "main.cpp]')
        self.assertEqual(message, 'CMD ["make", "main.cpp]')

    def is_instrucation_message_on_no_change(self):
        message = InstructionStep().get_change_message('CMD ["make", "main.cpp]')
        self.assertEqual(message, 'CMD ["make", "main.cpp]')
