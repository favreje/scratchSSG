import unittest
from htmlnode import HTMLNode


node1 = HTMLNode("body")
node2 = HTMLNode("div")
node3 = HTMLNode("p", "Hello world!")

TAG = "a"
VALUE = "Visit our homepage!"
CHILDREN = [node1, node2, node3]


class TestHTMLNode(unittest.TestCase):
    def test_single_prop(self):
        test_prop = {"href": "https://www.homepage.com"}
        result = ' href="https://www.homepage.com"'
        node = HTMLNode(tag=TAG, value=VALUE, children=CHILDREN, props=test_prop)
        test_node_prop = node.props_to_html()
        self.assertEqual(test_node_prop, result)

    def test_multiple_props(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        result = ' href="https://www.google.com" target="_blank"'
        test_node_prop = HTMLNode(TAG, VALUE, CHILDREN, test_props).props_to_html()
        self.assertEqual(test_node_prop, result)

    def test_many_props(self):
        test_props = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
        }

        result = ' 1="one" 2="two" 3="three" 4="four" 5="five"'
        test_node_prop = HTMLNode(TAG, VALUE, CHILDREN, test_props).props_to_html()
        self.assertEqual(test_node_prop, result)

    def test_empty_prop(self):
        test_props = {}
        test_node_prop = HTMLNode(TAG, VALUE, CHILDREN, test_props).props_to_html()
        result = ""
        self.assertEqual(test_node_prop, result)

    def test_empty_props(self):
        test_props = {"href": "https://www.homepage.com", "": ""}
        result = ' href="https://www.homepage.com"'
        test_node_props = HTMLNode(TAG, VALUE, CHILDREN, test_props).props_to_html()
        self.assertEqual(test_node_props, result)


if __name__ == "__main__":
    unittest.main()
