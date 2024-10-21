from enum import Enum, auto
import re


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown):
    raw_blocks = [block.strip() for block in markdown.split("\n\n")]
    return [block for block in raw_blocks if block]


def block_to_block_type(block):
    match = re.match(r"(#+)\s", block)
    if match and len(match.group(0)) <= 7:
        return BlockType.HEADING

    if re.match(r"^```([\s\S]*?)```(?=\Z)", block):
        return BlockType.CODE

    matches = re.match(r"^(>\s?.*(\n|\Z))+$", block)
    if matches:
        return BlockType.QUOTE

    matches = re.match(r"^([*-]\s+.+(\n|\Z))+$", block)
    if matches:
        return BlockType.UNORDERED_LIST

    if re.match(r"^(\d+\.\s+.+(\n|\Z))+$", block):
        numbers = re.findall(r"^(\d+)\.", block, re.MULTILINE)
        numbers = [int(num) for num in numbers]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def main():
    # ---- Preliminary Tests ----- #
    all_tests = [
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
    ]

    test_blocks = [
        "01. item\n02. item",
        "1. First item\n2. Second item\n Tricky third item - it's a cheeky monkey",
        "1. fixed it\n2. First item\n3. Second item\n4. Tricky because the list doesn't start with 1.",
        "```\nA true code block that is commented\n It also has\n multiple lines\n```",
    ]

    for block in test_blocks:
        print(f"{block}\n{block_to_block_type(block)}\n")


if __name__ == "__main__":
    main()
