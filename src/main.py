from textnode import TextNode
from htmlnode import HTMLNode 

# Just preliminary tests. To be removed after setting up the unit testing files
test_text = "Hello friend."
test_text_type = "ital"
test_url = "https://www.levco.net"
node = TextNode(test_text, test_text_type, test_url)
node2 = TextNode(test_text, test_text_type, test_url)

print(repr(node))
print(node == node2)

test_props = {
    "href": "https://www.google.com", 
    "target": "_blank",
}
test_htmlnode = HTMLNode("p", "Hello, friend.", props= test_props) 

try:
    rslt_html = test_htmlnode.to_html()
    print(rslt_html)
except NotImplementedError as e:
    print(f"Error: {e}")

rendered_props = test_htmlnode.props_to_html()
print("\nRendered HTML attributes:")
print(rendered_props)
print(repr(node))
print(repr(test_htmlnode))
