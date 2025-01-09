import unittest
from htmlNode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_parent_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "text")]).to_html()

    def test_parent_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]
                ),
                LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text</p><i>italic text</i></div>"
        )

    def test_parent_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "Hello")],
            {"class": "greeting"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="greeting">Hello</div>'
        )

if __name__ == "__main__":
    unittest.main()
