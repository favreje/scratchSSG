import unittest
from textnode import *

LARGE_NODE = TextNode(
    """ An *italic* markdown element, a **bold** markdown element, and a `code` markdown element
    walk into a bar. The bartender says, *"We don't serve italics* here." The `code` element
    replies, `Interface error: All declared types are valid and should be served. That is a known
    error that was previously logged in 2005. Please try again.` The **bold markdown element** adds
    "I would like to **heavily emphasize** that your comment is out of bounds, mister! The
    bartender then says, "Say less;  I'm having a **truly** bad night. I am *sincerely* sorry
    bros." The italic markdown element *accepts his apology*, and *the four of them* proceed to
    **hug it out.** By the end of the night, they were all *pre-rendered* **(AF!)** to **HTML**,
    the website loaded *much faster*, and they all lived happily ever after. `The End.`""",
    TEXT_TYPE_TEXT,
)

SMALL_NODE = TextNode("This is text with a `code block` word", TEXT_TYPE_TEXT)


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
        node = TextNode(
            "This is a text node with a longer line", "bold", "https://www.my_web_address.com"
        )
        node2 = TextNode(
            "This is a text node with a longer line", "bold", "https://www.my_web_address.com"
        )
        self.assertTrue(node == node2)

    def test_for_none(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", url=None)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", "normal", None)
        node2 = TextNode("This is a text node", "bold", url=None)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a test node", "bold", url=None)
        self.assertNotEqual(node, node2)

    def test_type_mismatch(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = ("This is a text node", "bold", None)
        self.assertNotEqual(node, node2)

    # --- split_nodes_delimiter function testing ---
    def test_split_with_exceptions(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([LARGE_NODE, SMALL_NODE], None, TEXT_TYPE_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([SMALL_NODE, LARGE_NODE], "*", TEXT_TYPE_BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([SMALL_NODE, LARGE_NODE], "*", "other")
        with self.assertRaises(Exception):
            delim_not_closed_node = TextNode("This is bold** text.", "bold")
            split_nodes_delimiter([delim_not_closed_node], "**", TEXT_TYPE_BOLD)

    def test_non_text_node(self):
        node = TextNode("Not a text_node.", "bold", "https://www.my_web_address.com")
        expected_result = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual([node], expected_result)

    def test_base_case(self):
        expected_result = [
            TextNode("This is text with a ", TEXT_TYPE_TEXT),
            TextNode("code block", TEXT_TYPE_CODE),
            TextNode(" word", TEXT_TYPE_TEXT),
        ]
        nodes = split_nodes_delimiter([SMALL_NODE], "`", "code")
        self.assertEqual(nodes, expected_result)

        node = TextNode("This contains **bold** text", "text")
        nodes = split_nodes_delimiter([node], "**", "bold")
        expected_result = [
            TextNode("This contains ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(nodes, expected_result)

        node = TextNode("This contains *italic* text", "text")
        nodes = split_nodes_delimiter([node], "*", "italic")
        expected_result = [
            TextNode("This contains ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text"),
        ]
        self.assertEqual(nodes, expected_result)

    def test_multiple_nodes(self):
        bold_node = TextNode("This contains **bold** text", "text")
        italic_node = TextNode("This contains *italic* text", "text")
        code_node = TextNode("This contains `code` text", "text")
        bold_split = split_nodes_delimiter([bold_node, italic_node, code_node], "**", "bold")
        italic_split = split_nodes_delimiter([bold_node, italic_node, code_node], "*", "italic")
        code_split = split_nodes_delimiter([bold_node, italic_node, code_node], "`", "code")
        expected_bold = [
            TextNode("This contains ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
            italic_node,
            code_node,
        ]
        expected_italic = [
            bold_node,
            TextNode("This contains ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text"),
            code_node,
        ]
        expected_code = [
            bold_node,
            italic_node,
            TextNode("This contains ", "text"),
            TextNode("code", "code"),
            TextNode(" text", "text"),
        ]

        self.assertEqual(bold_split, expected_bold)
        self.assertEqual(italic_split, expected_italic)
        self.assertEqual(code_split, expected_code)

    def test_combined_delimiters(self):
        node = TextNode("This is **bold** and this is *italic*", "text")
        bold_split_nodes = split_nodes_delimiter([node], "**", "bold")
        italic_split_nodes = split_nodes_delimiter([node], "*", "italic")
        expected_bold_result = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and this is *italic*", "text"),
        ]
        expected_italic_result = [
            TextNode("This is **bold** and this is ", "text"),
            TextNode("italic", "italic"),
        ]
        self.assertEqual(bold_split_nodes, expected_bold_result)
        self.assertEqual(italic_split_nodes, expected_italic_result)

    def test_edge_cases(self):
        bold_node = TextNode("This contains **double****bold** text", "text")
        bold_split_nodes = split_nodes_delimiter([bold_node], "**", "bold")
        bold_expected_result = [
            TextNode("This contains ", "text"),
            TextNode("double", "bold"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
        ]

        italic_node = TextNode("This contains *double* *italic* text", "text")
        italic_split_nodes = split_nodes_delimiter([italic_node], "*", "italic")
        italic_expected_result = [
            TextNode("This contains ", "text"),
            TextNode("double", "italic"),
            TextNode(" ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text"),
        ]

        beginning_bold_node = TextNode("**Bold** at the beginning", "text")
        beginning_split_nodes = split_nodes_delimiter([beginning_bold_node], "**", "bold")
        beginning_expected_result = [
            TextNode("Bold", "bold"),
            TextNode(" at the beginning", "text"),
        ]

        end_bold_node = TextNode("Bold at the **end**", "text")
        end_split_nodes = split_nodes_delimiter([end_bold_node], "**", "bold")
        end_expected_result = [
            TextNode("Bold at the ", "text"),
            TextNode("end", "bold"),
        ]

        self.assertEqual(bold_split_nodes, bold_expected_result)
        self.assertEqual(italic_split_nodes, italic_expected_result)
        self.assertEqual(beginning_split_nodes, beginning_expected_result)
        self.assertEqual(end_split_nodes, end_expected_result)


if __name__ == "__main__":
    unittest.main()
