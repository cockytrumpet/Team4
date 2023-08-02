import unittest
from frontend.helper import *

# test that invalid inputs are rejected


class Test(unittest.TestCase):
    def test_add_to_resources(self):
        # empty title
        message = add_to_resources("", "this_is_example", None, None)
        self.assertEqual(message[0], "error")
        # empty link
        message = add_to_resources("Test", "", None, None)
        self.assertEqual(message[0], "error")

    def test_update_resource(self):
        # empty title
        message = update_resource(1, "", "this_is_example", None, None, None)
        self.assertEqual(message[0], "error")
        # empty link
        message = update_resource(1, "Test", "", None, None, None)
        self.assertEqual(message[0], "error")

    def test_add_to_tags(self):
        # empty title
        message = add_to_tags("", "TestDescr", None)
        self.assertEqual(message[0], "error")

    def test_update_tag(self):
        # empty title
        message = update_tag(1, "", "TestDescr", None)
        self.assertEqual(message[0], "error")

    def test_add_to_projects(self):
        # empty title
        message = add_to_projects("", "TestDescr", None)
        self.assertEqual(message[0], "error")
