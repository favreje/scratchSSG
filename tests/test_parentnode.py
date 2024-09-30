import unittest
from htmlnode import *


# Total tests before this module: 16
# Total tests this module: 6
class TestParentNode(unittest.TestCase):

    def test_multiple_children(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "body",
                    [
                        ParentNode(
                            "div",
                            [
                                ParentNode(
                                    "p",
                                    [
                                        LeafNode("b", "Jeffrey Favret, "),
                                        LeafNode(None, "who is learning OOP "),
                                        LeafNode("i", "and "),
                                        LeafNode(None, "recursion, may be finally getting it!"),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )

        result = node.to_html()
        expectation = (
            "<html><body><div><p><b>Jeffrey Favret, </b>"
            "who is learning OOP <i>and </i>recursion, may "
            "be finally getting it!</p></div></body></html>"
        )
        self.assertEqual(result, expectation)

    def test_parent_after_leaf(self):
        node2 = ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")])
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Jeffrey Favret, "),
                LeafNode(None, "who is learning OOP "),
                LeafNode("i", "and "),
                LeafNode(None, "recursion, may be finally getting it!"),
                node2,
            ],
        )

        result = node.to_html()
        expectation = (
            "<p><b>Jeffrey Favret, </b>who is learning OOP <i>and "
            "</i>recursion, may be finally getting it!"
            "<ul><li>Item 1</li><li>Item 2</li></ul></p>"
        )
        self.assertEqual(result, expectation)

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode("", [LeafNode("", "Hello world.")])
            node.to_html()

    def test_no_child_left_behind(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p")
            node.to_html()

    def test_leaf_only(self):
        node = LeafNode("b", "Hello world.")
        result = node.to_html()
        expectation = "<b>Hello world.</b>"
        self.assertEqual(result, expectation)

    def test_only_child(self):
        node = ParentNode("div", [LeafNode("p", "Hello, friend.")])
        result = node.to_html()
        expectation = "<div><p>Hello, friend.</p></div>"
        self.assertEqual(result, expectation)
