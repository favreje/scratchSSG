import unittest
from markdown_to_html import *
from htmlnode import *


markdown_text = """
# Blog Post

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
> if you use them properly-they'll go through *anything*.
> You read and you're *pierced*.

## Second Point:

### Markdown can contain **various** in-line *code*, links and images

#### Here are a few useful links:

[boot-dot-dev](https://www.youtube.com/@bootdotdev)
[My home page](https://www.favreje.com)

#### And a funny image

![Rick has no F's to give](https://i.imgur.com/aKaOqIh.gif)

"""

markdown_text_missing_header = """
## Blog Post

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
> if you use them properly-they'll go through *anything*.
> You read and you're *pierced*.

## Second Point:

### Markdown can contain **various** in-line *code*, links and images

#### Here are a few useful links:

[boot-dot-dev](https://www.youtube.com/@bootdotdev)
[My home page](https://www.favreje.com)

#### And a funny image

![Rick has no F's to give](https://i.imgur.com/aKaOqIh.gif)

"""


class TestMarkdownToHTML(unittest.TestCase):
    def test_simple_case(self):
        md = """ A simple paragraph """
        node = markdown_to_html_node(md)
        expected_result = ParentNode(
            tag="div",
            children=[
                ParentNode(tag="p", children=[LeafNode(tag=None, value="A simple paragraph")])
            ],
        )
        self.assertEqual(node, expected_result)

    def test_two_md_objects(self):
        md = """
        # Header

        A simple paragraph

        """
        node = markdown_to_html_node(md)
        expected_result = ParentNode(
            tag="div",
            children=[
                ParentNode(tag="h1", children=[LeafNode(tag=None, value="Header")]),
                ParentNode(tag="p", children=[LeafNode(tag=None, value="A simple paragraph")]),
            ],
        )
        self.assertEqual(node, expected_result)

    def test_base_case(self):
        node = markdown_to_html_node(markdown_text)
        expected_result = ParentNode(
            tag="div",
            children=[
                ParentNode(tag="h1", children=[LeafNode(tag=None, value="Blog Post")]),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(
                            tag=None,
                            value="The main paragraph of my blog post will discuss the following points:",
                        )
                    ],
                ),
                ParentNode(
                    tag="ol",
                    children=[
                        ParentNode("li", children=[LeafNode(tag=None, value="Point number one")]),
                        ParentNode("li", children=[LeafNode(tag=None, value="Point number two")]),
                        ParentNode(
                            "li", children=[LeafNode(tag=None, value="Point number three")]
                        ),
                    ],
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(
                            tag=None,
                            value="And these unordered list items",
                        )
                    ],
                ),
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(
                            "li", children=[LeafNode(tag=None, value="First random thing")]
                        ),
                        ParentNode(
                            "li", children=[LeafNode(tag=None, value="Second random thing")]
                        ),
                        ParentNode(
                            "li", children=[LeafNode(tag=None, value="Third random thing")]
                        ),
                        ParentNode(
                            "li",
                            children=[
                                LeafNode(tag=None, value="Fourth random thing "),
                                LeafNode(tag="b", value="in no particular order"),
                            ],
                        ),
                    ],
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(
                            tag=None,
                            value="And it will contain the following code snippet:",
                        )
                    ],
                ),
                ParentNode(
                    tag="pre",
                    children=[
                        ParentNode(
                            tag="code",
                            children=[
                                LeafNode(
                                    tag=None,
                                    value='for i in range(10):\n    print("Hello world")',
                                )
                            ],
                        )
                    ],
                ),
                ParentNode(
                    tag="blockquote",
                    children=[
                        LeafNode(
                            tag=None,
                            value="Words can be like X-rays,\nif you use them properly-they'll go through ",
                        ),
                        LeafNode(tag="i", value="anything"),
                        LeafNode(tag=None, value=".\nYou read and you're "),
                        LeafNode(tag="i", value="pierced"),
                        LeafNode(tag=None, value="."),
                    ],
                ),
                ParentNode(tag="h2", children=[LeafNode(tag=None, value="Second Point:")]),
                ParentNode(
                    tag="h3",
                    children=[
                        LeafNode(tag=None, value="Markdown can contain "),
                        LeafNode(tag="b", value="various"),
                        LeafNode(tag=None, value=" in-line "),
                        LeafNode(tag="i", value="code"),
                        LeafNode(tag=None, value=", links and images"),
                    ],
                ),
                ParentNode(
                    tag="h4", children=[LeafNode(tag=None, value="Here are a few useful links:")]
                ),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(
                            tag="a",
                            value="boot-dot-dev",
                            props={"href": "https://www.youtube.com/@bootdotdev"},
                        ),
                        LeafNode(tag=None, value="\n"),
                        LeafNode(
                            tag="a",
                            value="My home page",
                            props={"href": "https://www.favreje.com"},
                        ),
                    ],
                ),
                ParentNode(tag="h4", children=[LeafNode(tag=None, value="And a funny image")]),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(
                            tag="img",
                            value="",
                            props={
                                "src": "https://i.imgur.com/aKaOqIh.gif",
                                "alt": "Rick has no F's to give",
                            },
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(node, expected_result)

    def test_extract_title(self):
        title = extract_title(markdown_text)
        expected_result = "Blog Post"
        self.assertEqual(title, expected_result)

    def test_exception(self):
        with self.assertRaises(HeaderNotFoundException):
            title = extract_title(markdown_text_missing_header)
            print(title)
