import unittest
from textnode import *
from inline_markdown import *

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

    # ----- Series of Tests for Extract Links and Extract Images -----
    def test_valid_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image = extract_markdown_images(text)
        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(image, expected_result)

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link = extract_markdown_links(text)
        expected_result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(link, expected_result)

    def test_single_link(self):
        text = "This is text with the infamous ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        image = extract_markdown_images(text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(image, expected_result)

        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        link = extract_markdown_links(text)
        expected_result = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(link, expected_result)

    def test_no_alt_text(self):
        text = "This is text with the infamous ![](https://i.imgur.com/aKaOqIh.gif)"
        image = extract_markdown_images(text)
        expected_result = [("", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(image, expected_result)

        text = "This is text with a link [](https://www.boot.dev)"
        link = extract_markdown_links(text)
        expected_result = [("https://www.boot.dev", "https://www.boot.dev")]
        self.assertEqual(link, expected_result)

    # ----- Series of Tests for Split Nodes Links -----
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TEXT_TYPE_TEXT,
        )
        node2 = TextNode(
            "[boot-dev](https://www.boot.dev) and a second link [to youtube](https://www.youtube.com/@bootdotdev)",
            TEXT_TYPE_TEXT,
        )
        node3 = TextNode(
            "Only url: [boot-dev](https://www.boot.dev)",
            TEXT_TYPE_TEXT,
        )

        node4 = TextNode(
            "[boot-dev](https://www.boot.dev) is the only url in my list.",
            TEXT_TYPE_TEXT,
        )

        node5 = TextNode(
            "[boot-dev](https://www.boot.dev)",
            TEXT_TYPE_TEXT,
        )

        node6 = TextNode(
            "There are no urls in my list.",
            TEXT_TYPE_TEXT,
        )

        node7 = TextNode(
            "This is text with a link [to my server](https://www.favreje.com) and [to youtube](https://www.youtube.com/@phreeville)",
            TEXT_TYPE_TEXT,
        )

        # Base case
        split_node = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", url="https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", url="https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_node, expected_result)

        # URL at beginning with other URLs
        split_node = split_nodes_link([node2])
        expected_result = [
            TextNode("boot-dev", "link", url="https://www.boot.dev"),
            TextNode(" and a second link ", "text"),
            TextNode("to youtube", "link", url="https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_node, expected_result)

        # Text, then One URL at end
        split_node = split_nodes_link([node3])
        expected_result = [
            TextNode("Only url: ", "text"),
            TextNode("boot-dev", "link", url="https://www.boot.dev"),
        ]
        self.assertEqual(split_node, expected_result)

        # One URL, then text
        split_node = split_nodes_link([node4])
        expected_result = [
            TextNode("boot-dev", "link", url="https://www.boot.dev"),
            TextNode(" is the only url in my list.", "text"),
        ]
        self.assertEqual(split_node, expected_result)

        # One URL, no text
        split_node = split_nodes_link([node5])
        expected_result = [
            TextNode("boot-dev", "link", url="https://www.boot.dev"),
        ]
        self.assertEqual(split_node, expected_result)

        # No URLs, text only
        split_node = split_nodes_link([node6])
        expected_result = [
            TextNode("There are no urls in my list.", "text"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes
        split_node = split_nodes_link([node, node7])
        expected_result = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", url="https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", url="https://www.youtube.com/@bootdotdev"),
            TextNode("This is text with a link ", "text"),
            TextNode("to my server", "link", url="https://www.favreje.com"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", url="https://www.youtube.com/@phreeville"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, second node no links
        split_node = split_nodes_link([node, node6])
        expected_result = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", url="https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", url="https://www.youtube.com/@bootdotdev"),
            TextNode("There are no urls in my list.", "text"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, no text between them
        split_node = split_nodes_link([node5, node5])
        expected_result = [
            TextNode("boot-dev", "link", url="https://www.boot.dev"),
            TextNode("boot-dev", "link", url="https://www.boot.dev"),
        ]
        self.assertEqual(split_node, expected_result)

    # ----- Series of Tests for Split Nodes Images -----
    def test_split_image(self):
        node = TextNode(
            "This is text with an image ![Rick doesn't care](https://i.imgur.com/aKaOqIh.gif) and another image ![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TEXT_TYPE_TEXT,
        )

        node2 = TextNode(
            "![Rick doesn't care](https://i.imgur.com/aKaOqIh.gif) and another image ![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TEXT_TYPE_TEXT,
        )

        node3 = TextNode(
            "Only image: ![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TEXT_TYPE_TEXT,
        )

        node4 = TextNode(
            "![Cute](https://i.imgur.com/rucw2JH.jpeg) is at the beginning.",
            TEXT_TYPE_TEXT,
        )

        node5 = TextNode(
            "![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TEXT_TYPE_TEXT,
        )

        node6 = TextNode(
            "There are no urls in my list.",
            TEXT_TYPE_TEXT,
        )

        node7 = TextNode(
            "Images of my dog: ![gus1](https://www.favreje.com/gus1.jpg) ![gus2](https://www.favreje.com/gus2.png)",
            TEXT_TYPE_TEXT,
        )

        # Base case
        split_node = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with an image ", "text"),
            TextNode("Rick doesn't care", "image", url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", "text"),
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        #  Image at beginning with other image
        split_node = split_nodes_image([node2])
        expected_result = [
            TextNode("Rick doesn't care", "image", url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", "text"),
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        # Text, then One image at end
        split_node = split_nodes_image([node3])
        expected_result = [
            TextNode("Only image: ", "text"),
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        # One image, then text
        split_node = split_nodes_image([node4])
        expected_result = [
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode(" is at the beginning.", "text"),
        ]
        self.assertEqual(split_node, expected_result)

        # One URL, no text
        split_node = split_nodes_image([node5])
        expected_result = [
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        # # No URLs, text only
        split_node = split_nodes_image([node6])
        expected_result = [
            TextNode("There are no urls in my list.", "text"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes
        split_node = split_nodes_image([node, node7])
        expected_result = [
            TextNode("This is text with an image ", "text"),
            TextNode("Rick doesn't care", "image", url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", "text"),
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode("Images of my dog: ", "text"),
            TextNode("gus1", "image", url="https://www.favreje.com/gus1.jpg"),
            TextNode(" ", "text"),
            TextNode("gus2", "image", url="https://www.favreje.com/gus2.png"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, second node no links
        split_node = split_nodes_image([node, node6])
        expected_result = [
            TextNode("This is text with an image ", "text"),
            TextNode("Rick doesn't care", "image", url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", "text"),
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode("There are no urls in my list.", "text"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, no text between them
        split_node = split_nodes_image([node5, node5])
        expected_result = [
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode("Cute", "image", url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

    # ----- Series of Tests for text_to_text_node function ----- #
    def test_base_level_text_conversion(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode(text="This is ", text_type="text"),
            TextNode(text="text", text_type="bold"),
            TextNode(text=" with an ", text_type="text"),
            TextNode(text="italic", text_type="italic"),
            TextNode(text=" word and a ", text_type="text"),
            TextNode(text="code block", text_type="code"),
            TextNode(text=" and an ", text_type="text"),
            TextNode(
                text="obi wan image", text_type="image", url="https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(text=" and a ", text_type="text"),
            TextNode(text="link", text_type="link", url="https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_result)

    def test_text_conversion_changed_order(self):
        text = "This is *italic text* with a **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode(text="This is ", text_type="text"),
            TextNode(text="italic text", text_type="italic"),
            TextNode(text=" with a ", text_type="text"),
            TextNode(text="bold", text_type="bold"),
            TextNode(text=" word and a ", text_type="text"),
            TextNode(text="code block", text_type="code"),
            TextNode(text=" and an ", text_type="text"),
            TextNode(
                text="obi wan image", text_type="image", url="https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(text=" and a ", text_type="text"),
            TextNode(text="link", text_type="link", url="https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_result)

    def test_text_conversion_with_text_only(self):
        text = "This is only text."
        nodes = text_to_textnodes(text)
        expected_result = [TextNode("This is only text.", "text")]
        self.assertEqual(nodes, expected_result)

    def test_text_conversion_link_first(self):
        text = "[link](https://boot.dev)"
        node = text_to_textnodes(text)
        expected_result = [TextNode("link", TEXT_TYPE_LINK, "https://boot.dev")]
        self.assertEqual(node, expected_result)

    def test_exception(self):
        with self.assertRaises(Exception):
            text = "Mismatched **bold."
            node = text_to_textnodes(text)
            return node


if __name__ == "__main__":
    unittest.main()
