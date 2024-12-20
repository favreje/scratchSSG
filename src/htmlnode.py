class HTMLNode:
    """
    Represents a node in an HTML document tree
        tag: str representing the HTML tag
        value: str representing
        children: list of HTMLNode objects representing the children of this node
        props: dict of name value pairs representing HTML attributes

    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag= '{self.tag}', value= '{self.value}', "
            f"children= {self.children}, props= {self.props})"
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        err_msg = f"Child classes will override this method to render themselves as HTML."
        raise NotImplementedError(err_msg)

    def props_to_html(self):
        if self.props:
            html_attrib = ""
            for key, value in self.props.items():
                if not key or not value:
                    continue
                html_attrib += f' {key}="{value}"'
            return html_attrib
        return ""


class LeafNode(HTMLNode):
    """
    Represents a single HTML tag with no children (i.e., the last node in an HTMLNode tree)
    Value is required (and cannot equal None) and tag is required (although it may equal None)
    """

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        tag_part = f"tag={repr(self.tag)}, " if self.tag is not None else ""
        props_part = f"props={repr(self.props)}" if self.props is not None else ""
        return f"LeafNode({tag_part}value={repr(self.value)}{props_part})"

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")

        # Check for self-closing tags, and handle accordingly
        if self.value == "":
            return f"<{self.tag}{self.props_to_html()}>"

        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    ParentNode(tag, children, [props])
    Handles nested HTML nodes. If an HTMLNode is not a LeafNode, (i.e., it has children) then it
    must be a ParentNode
    """

    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        children_part = f", children={self.children}" if self.children is not None else ""
        props_part = f", props={repr(self.props)}" if self.props is not None else ""

        return f"ParentNode({repr(self.tag)}{children_part}{props_part})"

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag is required for ParentNode objects.")
        if not self.children:
            raise ValueError("At least one child attribute is required for ParentNode objects.")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}>{self.props_to_html()}{children_html}</{self.tag}>"
