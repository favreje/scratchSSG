class HTMLNode:
    def __init__(self, tag= None, value= None, children= None, props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return (f"HTMLNode(tag= '{self.tag}', value= '{self.value}', "
            f"children= {self.children}, props= {self.props})")

    def to_html(self):
        err_msg = f"Child classes will override this method to render themselves as HTML."
        raise NotImplementedError(err_msg)

    def props_to_html(self):
        if self.props:
            html_attrib = ""
            for key, value in self.props.items():
                html_attrib += f" {key}=\"{value}\""
            return html_attrib
        return None
