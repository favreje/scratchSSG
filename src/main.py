from textnode import TextNode

test_text = "Hello friend."
test_text_type = "ital"
test_url = "https://www.levco.net"
my_node = TextNode(test_text, test_text_type, test_url)

print(repr(my_node))
