from textnode import *


def main():
    text_node = TextNode("Gus hanging out with his sister", "image", "gus_with_sister.jpg")
    leaf = text_node_to_html_node(text_node)
    result = leaf.to_html()
    print(result)

    node = TextNode("This is text with a `code block` word", TEXT_TYPE_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE_CODE)


if __name__ == "__main__":
    main()
