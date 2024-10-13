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
