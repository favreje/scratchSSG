import unittest
from htmlnode import LeafNode


# Test count = 16


class TestLeafNode(unittest.TestCase):
    def test_no_props(self):
        para_node = LeafNode("p", "This is a paragraph of text.")
        rendered_html = para_node.to_html()
        result = "<p>This is a paragraph of text.</p>"
        self.assertEqual(rendered_html, result)

    def test_with_props(self):
        link_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        rendered_html = link_node.to_html()
        result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(rendered_html, result)

    def test_with_no_tag(self):
        tagless_node = LeafNode(tag=None, value="This is unformatted text.")
        rendered_html = tagless_node.to_html()
        result = "This is unformatted text."
        self.assertEqual(rendered_html, result)

        tagless_node2 = LeafNode("", "This is unformatted text.")
        rendered_html2 = tagless_node2.to_html()
        self.assertEqual(rendered_html2, result)

    def test_missing_value(self):
        with self.assertRaises(ValueError):
            no_value_node = LeafNode(
                tag="a", value=None, props={"href": "https://www.google.com"}
            )
            no_value_node.to_html()
