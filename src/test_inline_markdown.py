import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        extracted_text = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            extracted_text,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images_empty(self):
        extracted_text = extract_markdown_images("")
        self.assertListEqual(extracted_text, [])

    def test_extract_markdown_links(self):
        extracted_text = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            extracted_text,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_markdown_links_empty(self):
        extracted_text = extract_markdown_links("")
        self.assertListEqual(extracted_text, [])

    def test_extract_markdown_links_wrong_syntax(self):
        # Testing malformed markdown link (missing square bracket)
        extracted_text = extract_markdown_links("This is a link (https://www.boot.dev)")
        self.assertListEqual(extracted_text, [])

        # Testing malformed markdown link (missing parentheses)
        extracted_text = extract_markdown_links("This is a link [to boot dev]")
        self.assertListEqual(extracted_text, [])

        # Testing a link without any markdown formatting
        extracted_text = extract_markdown_links("This is just a link: https://www.boot.dev")
        self.assertListEqual(extracted_text, [])

    def test_extract_markdown_images_wrong_syntax(self):
        # Testing malformed markdown image (missing square bracket)
        extracted_text = extract_markdown_images("This is an image (https://i.imgur.com/aKaOqIh.gif)")
        self.assertListEqual(extracted_text, [])

        # Testing malformed markdown image (missing parentheses)
        extracted_text = extract_markdown_images("This is an image ![rick roll]")
        self.assertListEqual(extracted_text, [])

        # Testing an image without any markdown formatting
        extracted_text = extract_markdown_images("This is just an image: https://i.imgur.com/aKaOqIh.gif")
        self.assertListEqual(extracted_text, [])
    
    def test_split_nodes_image_basic(self):
        node = TextNode("Hello ![alt](url) World", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" World", TextType.TEXT)
        ])

    def test_split_nodes_image_multiple(self):
        node = TextNode("![alt1](url1)middle![alt2](url2)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertListEqual(nodes, [
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode("middle", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2")
        ])

    def test_split_nodes_image_empty_alt(self):
        node = TextNode("Start ![](url) End", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertListEqual(nodes, [
            TextNode("Start ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "url"),
            TextNode(" End", TextType.TEXT)
        ])

    def test_split_nodes_link_basic(self):
        node = TextNode("Hello [label](url) World", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("label", TextType.LINK, "url"),
            TextNode(" World", TextType.TEXT)
        ])

    def test_split_nodes_link_multiple(self):
        node = TextNode("[label1](url1)mid[label2](url2)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [
            TextNode("label1", TextType.LINK, "url1"),
            TextNode("mid", TextType.TEXT),
            TextNode("label2", TextType.LINK, "url2")
        ])

    def test_split_nodes_link_image_text(self):
        node = TextNode("Hello ![not](a-link) [is](a-link)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [
           TextNode("Hello ![not](a-link) ", TextType.TEXT),
            TextNode("is", TextType.LINK, "a-link")
        ])

    def test_split_nodes_non_text(self):
        node = TextNode("[label](url)", TextType.BOLD)
        nodes = split_nodes_link([node])
        self.assertListEqual(nodes, [node])   

    def test_text_to_textnodes_basic(self):
        text = "Hello [link](url) and ![image](img_url)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img_url"),
            ],
        )

    def test_text_to_textnodes_formatting(self):
        text = "This is **bold**, *italic*, and `code`."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_nested(self):
        text = "Text with a [link](url) and an ![image](img_url)."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img_url"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_complex(self):
        text = "**Bold** and [link](url) with `code`."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_edge_cases(self):
        # Case with no special formatting
        text = "Plain text with no formatting."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes, [TextNode("Plain text with no formatting.", TextType.TEXT)]
        )

        # Case with malformed markdown
        text = "An [incomplete link]( and ![image missing parenthesis"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes, [TextNode(text, TextType.TEXT)]
        )

        # Empty string case
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [])

if __name__ == "__main__":
    unittest.main()
