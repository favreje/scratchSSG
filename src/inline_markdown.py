import re
from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delim = {TextType.BOLD: "**", TextType.ITALIC: "*", TextType.CODE: "`"}
    new_nodes = []
    for node in old_nodes:
        if text_type not in delim:
            raise Exception("Invalid text_type.")
        if delimiter != delim[text_type]:

            raise Exception("Delimiter argument does not match the text_type argument.")
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid mardown syntax: no closing delimiter for '{delimiter}'.")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text_builder = ""
            is_new_type = False
            i = 0
            text = node.text
            while i < len(text):
                if text_type == TextType.BOLD:
                    if i < len(text) - 1 and text[i] == "*" and text[i + 1] == "*":
                        if is_new_type == False:
                            is_new_type = True
                            current_type = node.text_type
                        else:
                            is_new_type = False
                            current_type = text_type
                        if text_builder:
                            new_nodes.append(TextNode(text_builder, current_type))
                            text_builder = ""
                        i += 2
                    else:
                        text_builder += text[i]
                        i += 1
                else:
                    if text[i] == delimiter:
                        if i < len(text) - 1 and text[i] == "*" and text[i + 1] == "*":
                            text_builder += "**"
                            i += 1
                        else:
                            if text[i] == delimiter:
                                if is_new_type == False:
                                    is_new_type = True
                                    current_type = node.text_type
                                else:
                                    is_new_type = False
                                    current_type = text_type
                                if text_builder:
                                    new_nodes.append(TextNode(text_builder, current_type))
                                    text_builder = ""
                    else:
                        text_builder += text[i]
                    i += 1
            if text_builder:
                current_type = text_type if is_new_type else node.text_type
                new_nodes.append(TextNode(text_builder, current_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    if matches:
        for i, match in enumerate(matches):
            if not match[0]:
                matches[i] = match[1], match[1]
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
        else:
            text = node.text
            for image_elements in images:
                image = f"![{image_elements[0]}]({image_elements[1]})"
                text_chunks = text.split(image, 1)
                if text_chunks[0]:
                    new_nodes.append(TextNode(text_chunks[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(image_elements[0], TextType.IMAGE, url=image_elements[1])
                )
                text = text_chunks[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
        else:
            text = node.text
            for link_elements in links:
                link = f"[{link_elements[0]}]({link_elements[1]})"
                text_chunks = text.split(link, 1)
                if text_chunks[0]:
                    new_nodes.append(TextNode(text_chunks[0], TextType.TEXT))
                new_nodes.append(TextNode(link_elements[0], TextType.LINK, url=link_elements[1]))
                text = text_chunks[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    markdown_elements = {"bold": "**", "italic": "*", "code": "`"}
    link_nodes = split_nodes_link([TextNode(text, TextType.TEXT)])
    image_nodes = split_nodes_image(link_nodes)
    bold_nodes = split_nodes_delimiter(image_nodes, markdown_elements["bold"], TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, markdown_elements["italic"], TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, markdown_elements["code"], TextType.CODE)
    return code_nodes
