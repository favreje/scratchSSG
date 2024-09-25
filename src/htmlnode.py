class HTMLNode:
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
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    ParentNode(tag, children, [props])
    Handles nested HTML nodes. Returns a string representing the HTML tag of the node and its
    children.
    """

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self, html_build={"prefix": "", "suffix": ""}):
        if not self.tag:
            raise ValueError("A tag is required for ParentNode objects.")
        if not self.children:
            raise ValueError("At least one child attribute is required for ParentNode objects.")

        html_build["prefix"] += f"<{self.tag}>"
        html_build["suffix"] = f"</{self.tag}>" + html_build["suffix"]
        for node in self.children:
            if isinstance(node, ParentNode):
                return node.to_html(html_build)
            html_build["prefix"] += node.to_html()
        return html_build["prefix"] + html_build["suffix"]


# -------------------------------------------------------------------------------------------------
# Initial test
# -------------------------------------------------------------------------------------------------
node = ParentNode(
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
)

node2 = ParentNode(
    "html",
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
)

result = node.to_html()
result2 = node2.to_html()
print(f"\n---\n{result}\n---")
print(f"\n---\n{result2}\n---")
