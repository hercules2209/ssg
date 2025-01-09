import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_identical_nodes(self):
        # Test two nodes with identical properties are equal
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        # Test nodes with different text are not equal
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_different_text_type(self):
        # Test nodes with different text types are not equal
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        # Test nodes with different URLs are not equal
        node1 = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.different.com")
        self.assertNotEqual(node1, node2)

    def test_eq_url_vs_no_url(self):
        # Test nodes where one has URL and other doesn't are not equal
        node1 = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_eq_none_url(self):
        # Test nodes with explicitly None URLs are equal
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
