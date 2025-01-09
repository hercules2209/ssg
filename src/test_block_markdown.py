import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, Block_Type, markdown_to_html_node
from htmlNode import ParentNode, LeafNode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_extra_newlines(self):
        markdown = """
# Heading with extra newlines


This is a paragraph.


"""
        expected_blocks = [
            "# Heading with extra newlines",
            "This is a paragraph.",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_no_blocks(self):
        markdown = ""
        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_single_block(self):
        markdown = "Just a single block without any blank lines."
        expected_blocks = ["Just a single block without any blank lines."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_whitespace_only(self):
        markdown = "\n\n   \n\n"
        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_heading_block(self):
        self.assertEqual(block_to_block_type("# Heading"), Block_Type.heading.value)
        self.assertEqual(block_to_block_type("###### Smallest Heading"), Block_Type.heading.value)
        self.assertNotEqual(block_to_block_type("####### Too Many Hashes"), Block_Type.heading.value)

    def test_code_block(self):
        code_block = """```
def hello_world():
    print("Hello, World!")
```"""
        self.assertEqual(block_to_block_type(code_block), Block_Type.code.value)

        not_code_block = """```
def hello_world():
    print("Hello, World!")
"""
        self.assertNotEqual(block_to_block_type(not_code_block), Block_Type.code.value)

    def test_quote_block(self):
        quote_block = """> This is a single-line quote."""
        self.assertEqual(block_to_block_type(quote_block), Block_Type.quote.value)

        multi_line_quote = """> Line one of quote\n> Line two of quote."""
        self.assertEqual(block_to_block_type(multi_line_quote), Block_Type.quote.value)

        not_quote = "> This is a quote\nBut this line is not."
        self.assertNotEqual(block_to_block_type(not_quote), Block_Type.quote.value)

    def test_unordered_list_block(self):
        unordered_list = """* Item 1\n* Item 2\n* Item 3"""
        self.assertEqual(block_to_block_type(unordered_list), Block_Type.unordered_list.value)

        mixed_list = """* Item 1\n- Item 2\n* Item 3"""
        self.assertEqual(block_to_block_type(mixed_list), Block_Type.unordered_list.value)

        not_unordered_list = """* Item 1\nNot a list item"""
        self.assertNotEqual(block_to_block_type(not_unordered_list), Block_Type.unordered_list.value)

    def test_ordered_list_block(self):
        ordered_list = """1. First item\n2. Second item\n3. Third item"""
        self.assertEqual(block_to_block_type(ordered_list), Block_Type.ordered_list.value)

        wrong_numbering = """1. First item\n3. Second item"""
        self.assertNotEqual(block_to_block_type(wrong_numbering), Block_Type.ordered_list.value)

        non_ordered_list = """1. First item\nSecond line not a list"""
        self.assertNotEqual(block_to_block_type(non_ordered_list), Block_Type.ordered_list.value)

    def test_paragraph_block(self):
        paragraph = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(paragraph), Block_Type.paragraph.value)

        multi_line_paragraph = """This is a paragraph with multiple lines.\nIt spans more than one line."""
        self.assertEqual(block_to_block_type(multi_line_paragraph), Block_Type.paragraph.value)

        not_paragraph = """# This is a heading"""
        self.assertNotEqual(block_to_block_type(not_paragraph), Block_Type.paragraph.value)



class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading_conversion(self):
        markdown = "# Heading"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[0].children[0].value, "Heading")

    def test_paragraph_conversion(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "p")
        self.assertEqual(html_node.children[0].children[0].value, "This is a paragraph.")

    def test_unordered_list_conversion(self):
        markdown = """* Item 1
* Item 2
* Item 3"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        ul_node = html_node.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 3)
        for i, li_node in enumerate(ul_node.children):
            self.assertEqual(li_node.tag, "li")
            self.assertEqual(li_node.children[0].value, f"Item {i + 1}")

    def test_ordered_list_conversion(self):
        markdown = """1. First item
2. Second item
3. Third item"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        ol_node = html_node.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)
        for i, li_node in enumerate(ol_node.children):
            self.assertEqual(li_node.tag, "li")
            self.assertEqual(li_node.children[0].value, f"{['First', 'Second', 'Third'][i]} item")

    def test_code_block_conversion(self):
        markdown = """```
print("Hello, World!")
```"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        pre_node = html_node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(code_node.children[0].value, 'print("Hello, World!")')

    def test_quote_block_conversion(self):
        markdown = """> This is a quote.
> Spanning multiple lines."""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        blockquote_node = html_node.children[0]
        self.assertEqual(blockquote_node.tag, "blockquote")
        self.assertEqual(blockquote_node.children[0].value, "This is a quote. Spanning multiple lines.")

    def test_combined_blocks(self):
        markdown = """# Heading

This is a paragraph.

* List item 1
* List item 2

> A quote block."""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 4)

        # Check heading
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[0].children[0].value, "Heading")

        # Check paragraph
        self.assertEqual(html_node.children[1].tag, "p")
        self.assertEqual(html_node.children[1].children[0].value, "This is a paragraph.")

        # Check unordered list
        ul_node = html_node.children[2]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 2)
        self.assertEqual(ul_node.children[0].children[0].value, "List item 1")
        self.assertEqual(ul_node.children[1].children[0].value, "List item 2")

        # Check quote block
        blockquote_node = html_node.children[3]
        self.assertEqual(blockquote_node.tag, "blockquote")
        self.assertEqual(blockquote_node.children[0].value, "A quote block.")

if __name__ == "__main__":
    unittest.main()
