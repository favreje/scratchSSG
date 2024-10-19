import unittest
from textnode import TextNode, text_node_to_html_node, TextType

# Total tests before this module: 22
# Total tests this module: 4


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_no_value(self):
        with self.assertRaises(ValueError):
            text_node = TextNode(text=None, text_type=TextType.TEXT)
            text_only_leaf = text_node_to_html_node(text_node)
            text_only_leaf.to_html()

    def test_invalid_text_type(self):
        with self.assertRaises(Exception):
            text_node = TextNode(text="Hello, Dolly!", text_type=PARAGRAPH)
            text_node_to_html_node(text_node)

        with self.assertRaises(Exception):
            text_node = TextNode(text="Hello, Dolly!", text_type=None)
            text_node_to_html_node(text_node)

        with self.assertRaises(Exception):
            text_node = TextNode(text="Hello, Dolly!", text_type="")
            text_node_to_html_node(text_node)

    def test_text_type_no_props(self):

        text_node = TextNode("Hello, friend.", TextType.TEXT)
        text_only_leaf = text_node_to_html_node(text_node)
        result = text_only_leaf.to_html()
        expectation = "Hello, friend."
        self.assertEqual(result, expectation)

        bold_node = TextNode("Hello, friend.", TextType.BOLD)
        bold_leaf = text_node_to_html_node(bold_node)
        result = bold_leaf.to_html()
        expectation = "<b>Hello, friend.</b>"
        self.assertEqual(result, expectation)

        ital_node = TextNode("Hello, friend.", TextType.ITALIC)
        ital_leaf = text_node_to_html_node(ital_node)
        result = ital_leaf.to_html()
        expectation = "<i>Hello, friend.</i>"
        self.assertEqual(result, expectation)

        code_node = TextNode("Hello, friend.", TextType.CODE)
        code_leaf = text_node_to_html_node(code_node)
        result = code_leaf.to_html()
        expectation = "<code>Hello, friend.</code>"
        self.assertEqual(result, expectation)

    def test_link_type(self):
        text_node = TextNode("Search the interwebs", TextType.LINK, "https://www.google.com")
        leaf = text_node_to_html_node(text_node)
        result = leaf.to_html()
        expectation = '<a href="https://www.google.com">Search the interwebs</a>'
        self.assertEqual(result, expectation)

    def test_image_type(self):
        text_node = TextNode(
            "Gus hanging out with his sister", TextType.IMAGE, "gus_with_sister.jpg"
        )
        leaf = text_node_to_html_node(text_node)
        result = leaf.to_html()
        expectation = '<img src="gus_with_sister.jpg" alt="Gus hanging out with his sister">'
        self.assertEqual(result, expectation)
