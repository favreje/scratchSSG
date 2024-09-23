# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


import unittest
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_all_attrib(self):
        node = TextNode("This is a text node", "bold", "https://www.my_web_address.com")
        node2 = TextNode("This is a text node", "bold", "https://www.my_web_address.com")
        self.assertEqual(node, node2)

    def test_eq_method(self):
        node = TextNode("This is a text node", "bold", "https://www.my_web_address.com")
        node2 = TextNode("This is a text node", "bold", "https://www.my_web_address.com")
        self.assertTrue(node == node2)

    def test_for_none(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", url= None)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", "normal", None)
        node2 = TextNode("This is a text node", "bold", url= None)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a test node", "bold", url= None)
        self.assertNotEqual(node, node2)

    def test_type_mismatch(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = ("This is a text node", "bold", None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
