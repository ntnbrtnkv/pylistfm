import unittest
import logging
from pylistfm.modes import string_to_mode


class ModesTests(unittest.TestCase):

    def test_string_to_mode(self):
        self.assertEqual(string_to_mode('s'), logging.NOTSET)
        self.assertEqual(string_to_mode('information'), logging.INFO)
