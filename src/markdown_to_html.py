from enum import Enum, auto
import re
from htmlnode import HTMLNode


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown: str):
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


def get_heading_level(block):
    match = re.match(r"(#+)\s(.+?)\s*$", block)
    if match:
        hashes, header_text = match.groups()
        if not header_text.strip():
            raise ValueError("Header must contain text")
        level = str(len(hashes))
        header = "h" + level
        header_text = header_text.strip()
        return header, header_text
    return None, None


def parse_markdown_list_items(block_type, block):
    if block_type not in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
        raise ValueError("BlockType must be ORDERED_LIST or UNORDERED_LIST.")
    children = []
    pattern = r"^[*-]\s+(.+)$" if block_type == BlockType.UNORDERED_LIST else r"^[0-9]+\.\s+(.+)$"
    match = re.finditer(pattern, block, re.MULTILINE)
    for m in match:
        li = m.group(1)
        children.append(HTMLNode(tag="li", value=li, children=None, props=None))
    return children


def block_to_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return HTMLNode(tag="p", value=block, children=None, props=None)
    if block_type == BlockType.HEADING:
        header, header_text = get_heading_level(block)
        return HTMLNode(tag=header, value=header_text, children=None, props=None)
    if block_type == BlockType.CODE:
        match = re.match(r"^```([\s\S]*?)```(?=\Z)", block)
        if match:
            code_text = match.groups()[0].strip()
        else:
            code_text = None
        child = HTMLNode(tag="code", value=code_text, children=None, props=None)
        return HTMLNode(tag="pre", value=None, children=[child], props=None)
    if block_type == BlockType.QUOTE:
        lines = re.findall(r"^>\s?(.*)", block, re.MULTILINE)
        text = "\n".join(lines)
        return HTMLNode(tag="blockquote", value=text, children=None, props=None)
    if block_type == BlockType.UNORDERED_LIST:
        children = parse_markdown_list_items(BlockType.UNORDERED_LIST, block)
        return HTMLNode(tag="ul", value=None, children=children, props=None)
    if block_type == BlockType.ORDERED_LIST:
        children = parse_markdown_list_items(BlockType.ORDERED_LIST, block)
        return HTMLNode(tag="ol", value=None, children=children, props=None)


def markdown_to_html_node(markdown):
    node_list = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = block_to_node(block)
        node_list.append(node)
    return HTMLNode(tag="div", value=None, children=node_list, props=None)


def main():
    markdown_test = """
# Blog Post

The main paragraph of my blog post will discuss the following points:

1. Point number one
2. Point number two
3. Point number three

And these unordered list items

- First random thing
- Second random thing
- Third random thing
- Fourth random thing (in no particular order)

And it will contain the following code snippet:

```
for i in range(10):
    print("Hello world")
```

> Words can be like X-rays,
> if you use them properly—they’ll go through anything.
> You read and you’re pierced.

## Second Point:

Markdown can contain **various** in-line *code*


"""

    main_node = markdown_to_html_node(markdown_test)
    print(main_node)
    print()
    for child in main_node.children:
        print(child)


if __name__ == "__main__":
    main()
