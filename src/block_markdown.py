from typing import List
from enum import Enum
from htmlNode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

class Block_Type(Enum):
    heading = "heading"
    paragraph = "paragraph"
    code ="code"
    quote ="quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Splits a Markdown string into blocks separated by blank lines.
    
    Args:
        markdown (str): The raw Markdown string representing a document.
    
    Returns:
        List[str]: A list of blocks, with leading and trailing whitespace stripped.
    """
    # Split by lines and handle whitespace
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks


def block_to_block_type(block: str) -> str:
    """
    Determines the type of a Markdown block.
    
    Args:
        block (str): A single block of Markdown text.
    
    Returns:
        str: The type of the block as a string.
    """

    lines = block.split("\n")

    if block.startswith("#") and 1 <= block.count("#", 0, block.find(" ")) <= 6:
        return Block_Type.heading.value

    if block.startswith("```") and block.endswith("```"):
        return Block_Type.code.value

    if all(line.startswith(">") for line in lines):
        return Block_Type.quote.value

    if all(line.startswith(("* ", "- ")) for line in lines):
        return Block_Type.unordered_list.value

    if all(line.split(". ", 1)[0].isdigit() and int(line.split(". ", 1)[0]) == idx + 1 for idx, line in enumerate(lines)):
        return Block_Type.ordered_list.value

    return Block_Type.paragraph.value

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == Block_Type.paragraph.value:
        return paragraph_to_html_node(block)
    if block_type == Block_Type.heading.value:
        return heading_to_html_node(block)
    if block_type == Block_Type.code.value:
        return code_to_html_node(block)
    if block_type == Block_Type.ordered_list.value:
        return olist_to_html_node(block)
    if block_type == Block_Type.unordered_list.value:
        return ulist_to_html_node(block)
    if block_type == Block_Type.quote.value:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3].strip()
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
