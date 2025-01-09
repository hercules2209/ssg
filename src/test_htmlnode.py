import unittest
from htmlNode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        # Test with no props
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        # Test with single prop
        node = HTMLNode("a", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" ')

    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(
            "a",
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        # Note: Since dictionaries don't maintain order, we need to check both possible orderings
        result = node.props_to_html()
        possible_outputs = [
            'href="https://www.google.com" target="_blank" ',
            'target="_blank" href="https://www.google.com" '
        ]
        self.assertIn(result, possible_outputs)

    def test_init_no_parameters(self):
        # Test initialization with no parameters
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_all_parameters(self):
        # Test initialization with all parameters
        props = {"class": "test-class"}
        children = [HTMLNode("span", "child")]
        node = HTMLNode("div", "parent", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

        

if __name__ == "__main__":
    unittest.main()
