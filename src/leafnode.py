from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props):
        super().__init__(tag= tag, value= value, children= None, props= props)

