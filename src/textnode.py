import enum
from htmlnode import LeafNode

# Constants
TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self) -> str:
        return f"TextNode(text= '{self.text}', text_type= '{self.text_type}', url= '{self.url}')"

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and self.text_type == other.text_type and self.url == other.url
        )


def text_node_to_html_node(text_node):

    if text_node.text_type == TEXT_TYPE_TEXT:
        return LeafNode(tag=None, value=text_node.text)

    if text_node.text_type == TEXT_TYPE_BOLD:
        return LeafNode(tag="b", value=text_node.text)

    if text_node.text_type == TEXT_TYPE_ITALIC:
        return LeafNode(tag="i", value=text_node.text)

    if text_node.text_type == TEXT_TYPE_CODE:
        return LeafNode(tag="code", value=text_node.text)

    if text_node.text_type == TEXT_TYPE_LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TEXT_TYPE_IMAGE:
        image_props = {"src": text_node.url, "alt": text_node.text}
        return LeafNode(tag="img", value="", props=image_props)

    else:
        raise Exception(
            f"{text_node.text_type} is not a valid text_type. Use one of the following:\n"
            f"'text', 'bold', 'italic', 'code', 'link', or 'image'"
        )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def create_text_nodes(node_parts):
        new_nodes = []
        for i, part in enumerate(node_parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, node.text_type))
            else:
                new_nodes.append(TextNode(part, text_type))
        return new_nodes

    delim = {"bold": "**", "italic": "*", "code": "`"}
    new_nodes = []
    for node in old_nodes:
        if delimiter != delim[text_type]:
            raise Exception("Delimiter argument does not match the text_type argument.")
        if not delimiter in node.text:
            raise Exception(f"Delimter {delimiter}: not found in the text argument.")
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid mardown syntax: no closing delimiter for '{delimiter}'.")

        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
        else:
            node_parts = node.text.split(delim[text_type])
            if text_type != TEXT_TYPE_ITALIC:
                new_nodes.extend(create_text_nodes(node_parts))

            else:
                i = 0
                builder = []
                while i < len(node_parts):
                    if i < len(node_parts) - 1 and node_parts[i + 1] == "":  # Double asterisk case
                        builder.append(
                            node_parts[i] + "**" + node_parts[i + 2] + "**" + node_parts[i + 4]
                        )
                        i += 5
                    else:
                        builder.append(node_parts[i])
                        i += 1

                print(builder)
                new_nodes.extend(create_text_nodes(builder))

    return new_nodes


node = TextNode("This is **bold** text **with** an *italic* word", TEXT_TYPE_TEXT)
new_nodes = split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC)

# for i, node in enumerate(new_nodes):
#     # print(f"{i}: '{node.text}', '{node.text_type}'")
#     print([node.text, node.text_type])
