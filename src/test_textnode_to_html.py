import unittest
from textnode import TextNode, TextType
from htmlNode import LeafNode
from main import text_node_to_html_node

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_conversion(self):
        # Test regular text conversion
        node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertIsNone(html_node.tag)
        self.assertIsNone(html_node.props)

    def test_bold_conversion(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_conversion(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_conversion(self):
        node = TextNode("Code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code block")

    def test_link_conversion(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props["href"], "https://www.example.com")

    def test_image_conversion(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "image.jpg")
        self.assertEqual(html_node.props["alt"], "Alt text")

    def test_invalid_type_conversion(self):
        # Test that invalid types raise an exception
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("Invalid", "invalid_type"))

if __name__ == '__main__':
    unittest.main()
