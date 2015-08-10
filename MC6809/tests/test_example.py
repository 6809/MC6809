
import unittest

from MC6809.example6809 import run_example

class ExampleTestCase(unittest.TestCase):
    def test_example(self):
        self.assertTrue(run_example())
