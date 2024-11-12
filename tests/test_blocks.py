import unittest

from markdown_to_html import BlockType, markdown_to_blocks, block_to_block_type


# ----- Test Data ----- #
markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

markdown2 = """
# This is a heading



## This is a subheader




This is a paragraph of text. It has some **bold** and *italic* words inside of it.

"""
markdown3 = """
     # This is a heading     



                ## This is a subheader  




This is a paragraph of text. It has some **bold** and *italic* words inside
of it.         

     
    
"""
# ---- Bock Type  Test Data ----- #
block_type_test_data = [
    "###### My Header",
    "# Jeff's Code",
    "####### Too long to be a header",
    "Words before ## This Header",
    "## A sub-header ##",
    "#Not a header because no space",
    "```# An inline block of code that is commented ```, followed by a **bold** word.",
    "Preceded text ```# An inline block of code because of preceeding text.```",
    "```# A true code block that is commented\n It also has\n multiple lines```",
    "```\nA true code block that is commented\n It also has\n multiple lines\n```",
    "> 'This would be quoted text.'",
    ">What if no space?",
    "> 'This would also be quoted text.\n> Because each line has the quote character'\n",
    "> 'This would not.\nBecause it needs the proper character on each line.'",
    "* First item\n* Second item",
    "* First item\n* Second item\n Tricky third item - it's a cheeky monkey",
    "* First item\n* Second item\n- Tricky third item - it's a cheeky monkey",
    "01. item\n02. item",
    "1. First item\n2. Second item\n Tricky third item - it's a cheeky monkey",
    "1. fixed it\n2. First item\n3. Second item\n4. Tricky because the list doesn't start with 1.",
    "```\nA true code block that is commented\n It also has\n multiple lines\n```",
]


class TestTextNode(unittest.TestCase):
    def test_base_case(self):
        blocks = markdown_to_blocks(markdown)
        expected_result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(blocks, expected_result)

    def test_redundant_newlines(self):
        blocks = markdown_to_blocks(markdown2)
        expected_result = [
            "# This is a heading",
            "## This is a subheader",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        ]
        self.assertEqual(blocks, expected_result)

    def test_white_space(self):
        blocks = markdown_to_blocks(markdown3)
        expected_result = [
            "# This is a heading",
            "## This is a subheader",
            "This is a paragraph of text. It has some **bold** and *italic* words inside\nof it.",
        ]
        self.assertEqual(blocks, expected_result)

    # ----- Testing Block Types -----
    def test_block_heading(self):
        heading_data = [
            "###### Long Header",
            "# Single Header",
            "####### Too long to be a header",
            "Words before ## This Header",
            "## A sub-header ##",
            "##      More than one space",
            "#Not a header because no space",
        ]
        test_types = [block_to_block_type(block) for block in heading_data]
        expected_types = [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual(test_types, expected_types)

    def test_block_code(self):
        code_data = [
            "```# An inline block of code that is commented ```, followed by a **bold** word.",
            "Preceded text ```# An inline block of code because of preceeding text.```",
            "```# A true code block that is commented\n It also has\n multiple lines```",
            "```\nA true code block that is commented\n It also has\n multiple lines\n```",
        ]
        test_types = [block_to_block_type(block) for block in code_data]
        expected_types = [
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.CODE,
            BlockType.CODE,
        ]
        self.assertEqual(test_types, expected_types)

    def test_block_quote(self):
        quote_data = [
            "> 'This would be quoted text.'",
            ">What if no space?",
            "> 'This would also be quoted text.\n>Because each line has the quote character'\n>",
            "> 'This would not.\nBecause it needs the proper character on each line.'",
            ">              This would be okay, even with massive amounts of whitespace",
        ]
        test_types = [block_to_block_type(block) for block in quote_data]
        expected_types = [
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.QUOTE,
            BlockType.PARAGRAPH,
            BlockType.QUOTE,
        ]
        self.assertEqual(test_types, expected_types)

    def test_block_unordered_list(self):
        unordered_list_data = [
            "* First item\n* Second item",
            "* First item\n* Second item\n Tricky third item with no number - it's a cheeky monkey",
            "* First item\n* Second item\n- Tricky third item with a different symbol",
            "* First item\n*Second item has no space, so it's a paragraph",
        ]
        test_types = [block_to_block_type(block) for block in unordered_list_data]
        expected_types = [
            BlockType.UNORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual(test_types, expected_types)

    def test_block_ordered_list(self):
        ordered_list_data = [
            "01. item\n02. item - leading zeros are okay",
            "1. First item\n2. Second item\n Tricky third item - no number",
            "1. Item one \n2. Item two\n3. Item three\n4. Item 4 - longer list",
            "1. Item one \n2. Item two\n3. Item three\n5. Item 4 - is misnumbered",
            "1. Item one \n2. Item two\n2. Item two\n3. Item three - number 2 is used twice",
            "1 Item one \n2. Item two - No period after items one",
            "1. Item one \n2. Item two \n3. 3",
            "1. Item one \n2. Item two \n 3. White space before item 3",
        ]
        test_types = [block_to_block_type(block) for block in ordered_list_data]
        expected_types = [
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual(test_types, expected_types)
