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
    TextType.TEXT,
)

SMALL_NODE = TextNode("This is text with a `code block` word", TextType.TEXT)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_all_attrib(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.my_web_address.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.my_web_address.com")
        self.assertEqual(node, node2)

    def test_eq_method(self):
        node = TextNode(
            "This is a text node with a longer line",
            TextType.BOLD,
            "https://www.my_web_address.com",
        )
        node2 = TextNode(
            "This is a text node with a longer line",
            TextType.BOLD,
            "https://www.my_web_address.com",
        )
        self.assertTrue(node == node2)

    def test_for_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", "normal", None)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a test node", TextType.BOLD, url=None)
        self.assertNotEqual(node, node2)

    def test_type_mismatch(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = ("This is a text node", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

    # --- split_nodes_delimiter function testing ---
    def test_split_with_exceptions(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([LARGE_NODE, SMALL_NODE], None, TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([SMALL_NODE, LARGE_NODE], "*", TextType.BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([SMALL_NODE, LARGE_NODE], "*", "other")
        with self.assertRaises(Exception):
            delim_not_closed_node = TextNode("This is bold** text.", TextType.BOLD)
            split_nodes_delimiter([delim_not_closed_node], "**", TextType.BOLD)

    def test_non_text_node(self):
        node = TextNode("Not a text_node.", TextType.BOLD, "https://www.my_web_address.com")
        expected_result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([node], expected_result)

    def test_base_case(self):
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        nodes = split_nodes_delimiter([SMALL_NODE], "`", TextType.CODE)
        self.assertEqual(nodes, expected_result)

        node = TextNode("This contains **bold** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_result)

        node = TextNode("This contains *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_result = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_result)

    def test_multiple_nodes(self):
        bold_node = TextNode("This contains **bold** text", TextType.TEXT)
        italic_node = TextNode("This contains *italic* text", TextType.TEXT)
        code_node = TextNode("This contains `code` text", TextType.TEXT)
        bold_split = split_nodes_delimiter(
            [bold_node, italic_node, code_node], "**", TextType.BOLD
        )
        italic_split = split_nodes_delimiter(
            [bold_node, italic_node, code_node], "*", TextType.ITALIC
        )
        code_split = split_nodes_delimiter([bold_node, italic_node, code_node], "`", TextType.CODE)
        expected_bold = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            italic_node,
            code_node,
        ]
        expected_italic = [
            bold_node,
            TextNode("This contains ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            code_node,
        ]
        expected_code = [
            bold_node,
            italic_node,
            TextNode("This contains ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(bold_split, expected_bold)
        self.assertEqual(italic_split, expected_italic)
        self.assertEqual(code_split, expected_code)

    def test_combined_delimiters(self):
        node = TextNode("This is **bold** and this is *italic*", TextType.TEXT)
        bold_split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        italic_split_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_bold_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is *italic*", TextType.TEXT),
        ]
        expected_italic_result = [
            TextNode("This is **bold** and this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(bold_split_nodes, expected_bold_result)
        self.assertEqual(italic_split_nodes, expected_italic_result)

    def test_edge_cases(self):
        bold_node = TextNode("This contains **double****bold** text", TextType.TEXT)
        bold_split_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        bold_expected_result = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("double", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        italic_node = TextNode("This contains *double* *italic* text", TextType.TEXT)
        italic_split_nodes = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        italic_expected_result = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("double", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        beginning_bold_node = TextNode("**Bold** at the beginning", TextType.TEXT)
        beginning_split_nodes = split_nodes_delimiter([beginning_bold_node], "**", TextType.BOLD)
        beginning_expected_result = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the beginning", TextType.TEXT),
        ]

        end_bold_node = TextNode("Bold at the **end**", TextType.TEXT)
        end_split_nodes = split_nodes_delimiter([end_bold_node], "**", TextType.BOLD)
        end_expected_result = [
            TextNode("Bold at the ", TextType.TEXT),
            TextNode("end", TextType.BOLD),
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
            TextType.TEXT,
        )
        node2 = TextNode(
            "[boot-dev](https://www.boot.dev) and a second link [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node3 = TextNode(
            "Only url: [boot-dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        node4 = TextNode(
            "[boot-dev](https://www.boot.dev) is the only url in my list.",
            TextType.TEXT,
        )

        node5 = TextNode(
            "[boot-dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        node6 = TextNode(
            "There are no urls in my list.",
            TextType.TEXT,
        )

        node7 = TextNode(
            "This is text with a link [to my server](https://www.favreje.com) and [to youtube](https://www.youtube.com/@phreeville)",
            TextType.TEXT,
        )

        # Base case
        split_node = split_nodes_link([node])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_node, expected_result)

        # URL at beginning with other URLs
        split_node = split_nodes_link([node2])
        expected_result = [
            TextNode("boot-dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and a second link ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(split_node, expected_result)

        # Text, then One URL at end
        split_node = split_nodes_link([node3])
        expected_result = [
            TextNode("Only url: ", TextType.TEXT),
            TextNode("boot-dev", TextType.LINK, url="https://www.boot.dev"),
        ]
        self.assertEqual(split_node, expected_result)

        # One URL, then text
        split_node = split_nodes_link([node4])
        expected_result = [
            TextNode("boot-dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" is the only url in my list.", TextType.TEXT),
        ]
        self.assertEqual(split_node, expected_result)

        # One URL, no text
        split_node = split_nodes_link([node5])
        expected_result = [
            TextNode("boot-dev", TextType.LINK, url="https://www.boot.dev"),
        ]
        self.assertEqual(split_node, expected_result)

        # No URLs, text only
        split_node = split_nodes_link([node6])
        expected_result = [
            TextNode("There are no urls in my list.", TextType.TEXT),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes
        split_node = split_nodes_link([node, node7])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to my server", TextType.LINK, url="https://www.favreje.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@phreeville"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, second node no links
        split_node = split_nodes_link([node, node6])
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
            TextNode("There are no urls in my list.", TextType.TEXT),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, no text between them
        split_node = split_nodes_link([node5, node5])
        expected_result = [
            TextNode("boot-dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode("boot-dev", TextType.LINK, url="https://www.boot.dev"),
        ]
        self.assertEqual(split_node, expected_result)

    # ----- Series of Tests for Split Nodes Images -----
    def test_split_image(self):
        node = TextNode(
            "This is text with an image ![Rick doesn't care](https://i.imgur.com/aKaOqIh.gif) and another image ![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TextType.TEXT,
        )

        node2 = TextNode(
            "![Rick doesn't care](https://i.imgur.com/aKaOqIh.gif) and another image ![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TextType.TEXT,
        )

        node3 = TextNode(
            "Only image: ![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TextType.TEXT,
        )

        node4 = TextNode(
            "![Cute](https://i.imgur.com/rucw2JH.jpeg) is at the beginning.",
            TextType.TEXT,
        )

        node5 = TextNode(
            "![Cute](https://i.imgur.com/rucw2JH.jpeg)",
            TextType.TEXT,
        )

        node6 = TextNode(
            "There are no urls in my list.",
            TextType.TEXT,
        )

        node7 = TextNode(
            "Images of my dog: ![gus1](https://www.favreje.com/gus1.jpg) ![gus2](https://www.favreje.com/gus2.png)",
            TextType.TEXT,
        )

        # Base case
        split_node = split_nodes_image([node])
        expected_result = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("Rick doesn't care", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        #  Image at beginning with other image
        split_node = split_nodes_image([node2])
        expected_result = [
            TextNode("Rick doesn't care", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        # Text, then One image at end
        split_node = split_nodes_image([node3])
        expected_result = [
            TextNode("Only image: ", TextType.TEXT),
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        # One image, then text
        split_node = split_nodes_image([node4])
        expected_result = [
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode(" is at the beginning.", TextType.TEXT),
        ]
        self.assertEqual(split_node, expected_result)

        # One URL, no text
        split_node = split_nodes_image([node5])
        expected_result = [
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

        # # No URLs, text only
        split_node = split_nodes_image([node6])
        expected_result = [
            TextNode("There are no urls in my list.", TextType.TEXT),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes
        split_node = split_nodes_image([node, node7])
        expected_result = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("Rick doesn't care", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode("Images of my dog: ", TextType.TEXT),
            TextNode("gus1", TextType.IMAGE, url="https://www.favreje.com/gus1.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("gus2", TextType.IMAGE, url="https://www.favreje.com/gus2.png"),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, second node no links
        split_node = split_nodes_image([node, node6])
        expected_result = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("Rick doesn't care", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode("There are no urls in my list.", TextType.TEXT),
        ]
        self.assertEqual(split_node, expected_result)

        # Two nodes, no text between them
        split_node = split_nodes_image([node5, node5])
        expected_result = [
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
            TextNode("Cute", TextType.IMAGE, url="https://i.imgur.com/rucw2JH.jpeg"),
        ]
        self.assertEqual(split_node, expected_result)

    # ----- Series of Tests for text_to_text_node function ----- #
    def test_base_level_text_conversion(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode(text="This is ", text_type=TextType.TEXT),
            TextNode(text="text", text_type=TextType.BOLD),
            TextNode(text=" with an ", text_type=TextType.TEXT),
            TextNode(text="italic", text_type=TextType.ITALIC),
            TextNode(text=" word and a ", text_type=TextType.TEXT),
            TextNode(text="code block", text_type=TextType.CODE),
            TextNode(text=" and an ", text_type=TextType.TEXT),
            TextNode(
                text="obi wan image",
                text_type=TextType.IMAGE,
                url="https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(text=" and a ", text_type=TextType.TEXT),
            TextNode(text="link", text_type=TextType.LINK, url="https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_result)

    def test_text_conversion_changed_order(self):
        text = "This is *italic text* with a **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode(text="This is ", text_type=TextType.TEXT),
            TextNode(text="italic text", text_type=TextType.ITALIC),
            TextNode(text=" with a ", text_type=TextType.TEXT),
            TextNode(text="bold", text_type=TextType.BOLD),
            TextNode(text=" word and a ", text_type=TextType.TEXT),
            TextNode(text="code block", text_type=TextType.CODE),
            TextNode(text=" and an ", text_type=TextType.TEXT),
            TextNode(
                text="obi wan image",
                text_type=TextType.IMAGE,
                url="https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(text=" and a ", text_type=TextType.TEXT),
            TextNode(text="link", text_type=TextType.LINK, url="https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_result)

    def test_text_conversion_with_text_only(self):
        text = "This is only text."
        nodes = text_to_textnodes(text)
        expected_result = [TextNode("This is only text.", TextType.TEXT)]
        self.assertEqual(nodes, expected_result)

    def test_text_conversion_link_first(self):
        text = "[link](https://boot.dev)"
        node = text_to_textnodes(text)
        expected_result = [TextNode("link", TextType.LINK, "https://boot.dev")]
        self.assertEqual(node, expected_result)

    def test_exception(self):
        with self.assertRaises(Exception):
            text = "Mismatched **bold."
            node = text_to_textnodes(text)
            return node


if __name__ == "__main__":
    unittest.main()
