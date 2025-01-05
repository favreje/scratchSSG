from enum import Enum, auto
import re
from htmlnode import ParentNode, HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class HeaderNotFoundException(Exception):
    pass


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

    matches = re.match(r"^(\s*>\s*.*(\n|\Z))+$", block)
    if matches:
        return BlockType.QUOTE

    matches = re.match(r"^(\s*[*-]\s+.+(\n|\Z))+$", block)
    if matches:
        return BlockType.UNORDERED_LIST

    if re.match(r"^(\s*\d+\.\s+.+(\n|\Z))+$", block):
        numbers = re.findall(r"^\s*(\d+)\.", block, re.MULTILINE)
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
    list_items = []
    pattern = (
        r"^\s*[*-]\s+(.+)$" if block_type == BlockType.UNORDERED_LIST else r"^\s*[0-9]+\.\s+(.+)$"
    )
    match = re.finditer(pattern, block, re.MULTILINE)
    for m in match:
        text = m.group(1)
        children = text_to_children(text)
        list_items.append(ParentNode(tag="li", children=children))
    return list_items


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(child) for child in text_nodes]
    return children


def block_to_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(block)
        node = ParentNode(tag="p", children=children)
        return node
    if block_type == BlockType.HEADING:
        header, header_text = get_heading_level(block)
        children = text_to_children(header_text)
        node = ParentNode(tag=header, children=children)
        return node
    if block_type == BlockType.CODE:
        match = re.match(r"^```([\s\S]*?)```(?=\Z)", block)
        if match:
            code_text = match.groups()[0].strip()
        else:
            code_text = None
        children = text_to_children(code_text)
        code_child = [ParentNode(tag="code", children=children)]
        node = ParentNode(tag="pre", children=code_child)
        return node
    if block_type == BlockType.QUOTE:
        lines = re.findall(r"^\s*>\s*(.*)", block, re.MULTILINE)
        text = "\n".join(lines)
        children = text_to_children(text)
        node = ParentNode(tag="blockquote", children=children)
        return node
    if block_type == BlockType.UNORDERED_LIST:
        children = parse_markdown_list_items(BlockType.UNORDERED_LIST, block)
        node = ParentNode(tag="ul", children=children)
        return node
    if block_type == BlockType.ORDERED_LIST:
        children = parse_markdown_list_items(BlockType.ORDERED_LIST, block)
        node = ParentNode(tag="ol", children=children)
        return node


def markdown_to_html_node(markdown):
    node_list = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = block_to_node(block)
        node_list.append(node)
    return ParentNode(tag="div", children=node_list)


def extract_title(markdown):
    """
    Pulls the h1 header from the markdown file (the line that starts with a single #) and returns
    the stripped text title.

    Although not explicitly stated in the project requirements, the function assumes that only the
    first h1 header encountered will be returned.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            heading_level, heading_text = get_heading_level(block)
            if heading_level == "h1":
                return heading_text
    raise HeaderNotFoundException("No H1 header found in markdown content")


def main():
    markdown_text = """

# Jeffrey's Personal Diary

The main paragraph of my blog post will discuss the following points:

1. Point number one
2. Point number two
3. Point number three

And these unordered list items

- First random thing
- Second random thing
- Third random thing
- Fourth random thing **in no particular order**

And it will contain the following code snippet:

```
for i in range(10):
    print("Hello world")
```

> Words can be like X-rays,
> if you use them properly—they’ll go through *anything*.
> You read and you’re *pierced*.

## Second Point:

### Markdown can contain **various** in-line *code*, links and images

#### Here are a few useful links:

[boot-dot-dev](https://www.youtube.com/@bootdotdev)
[My home page](https://www.favreje.com)

#### And some funny images

![Rick has no F's to give](https://i.imgur.com/aKaOqIh.gif)



"""

    # main_node = markdown_to_html_node(markdown_text)
    # for child in main_node.children:
    #     print(child.tag)
    #     print(child.children)
    #     print()
    #
    # print("----------")
    # print(main_node)

    print()
    test = extract_title(markdown_text)
    print(repr(test))


if __name__ == "__main__":
    main()
