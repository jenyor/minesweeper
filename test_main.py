import unittest
import main


class UnitTests(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(main.hello_world(), "Hello World")
