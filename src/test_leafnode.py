import unittest
from htmlNode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_tag(self):
        # Test node with just value, no tag
        node = LeafNode(value="Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_paragraph(self):
        # Test basic paragraph tag
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_with_props(self):
        # Test node with properties (link)
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_none_value(self):
        # Test that None value raises ValueError
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_multiple_props(self):
        # Test node with multiple properties
        node = LeafNode(
            "a",
            "Click me!",
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        # Since dict order isn't guaranteed, check for both possible orderings
        possible_outputs = [
            '<a href="https://www.google.com" target="_blank">Click me!</a>',
            '<a target="_blank" href="https://www.google.com">Click me!</a>'
        ]
        self.assertIn(node.to_html(), possible_outputs)

    def test_empty_props(self):
        # Test node with empty props dict
        node = LeafNode("p", "Text", {})
        self.assertEqual(node.to_html(), "<p>Text</p>")

    def test_repr(self):
        # Test string representation
        node = LeafNode("p", "Text")
        self.assertEqual(
            repr(node),
            'HTMLNode(tag=p, value=Text, children=None, props=None)'
        )

if __name__ == "__main__":
    unittest.main()
