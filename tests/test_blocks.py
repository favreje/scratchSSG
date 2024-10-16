import unittest
from blocks import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_base_case(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(blocks, expected_result)

    def test_redundant_newlines(self):
        markdown = """
# This is a heading



## This is a subheader




This is a paragraph of text. It has some **bold** and *italic* words inside of it.

"""
        blocks = markdown_to_blocks(markdown)
        expected_result = [
            "# This is a heading",
            "## This is a subheader",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        ]
        self.assertEqual(blocks, expected_result)

    def test_white_space(self):
        markdown = """
     # This is a heading     



                ## This is a subheader  




This is a paragraph of text. It has some **bold** and *italic* words inside
of it.         

     
    
"""
        blocks = markdown_to_blocks(markdown)
        expected_result = [
            "# This is a heading",
            "## This is a subheader",
            "This is a paragraph of text. It has some **bold** and *italic* words inside\nof it.",
        ]
        self.assertEqual(blocks, expected_result)
