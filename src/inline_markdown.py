from textnode import TextType, TextNode
from typing import List, Tuple
import re

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Split text nodes based on a delimiter and convert the delimited text to a specified type.
    
    Args:
        old_nodes: List of TextNode objects to process
        delimiter: String delimiter to split on (e.g., "`", "**", "*")
        text_type: TextType to apply to delimited text
        
    Returns:
        List of new TextNode objects with delimited text converted to specified type
        
    Raises:
        ValueError: If delimiter pairs are unmatched
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split text nodes containing markdown image syntax into separate text and image nodes.
    
    Args:
        old_nodes: A list of TextNode objects to process. Only nodes of type TEXT will be checked for images.
    
    Returns:
        A list of TextNode objects where markdown images are split into separate IMAGE nodes.
        
    Behavior:
        - Identifies image syntax in the form `![alt text](image_url)` within TEXT nodes.
        - Splits text before, between, and after image syntax into separate TEXT nodes.
        - Converts image syntax into IMAGE nodes with `alt text` as the text and `image_url` as the URL.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            remaining_text = parts[1] if len(parts) > 1 else ""
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split text nodes containing markdown link syntax into separate text and link nodes.
    
    Args:
        old_nodes: A list of TextNode objects to process. Only nodes of type TEXT will be checked for links.
    
    Returns:
        A list of TextNode objects where markdown links are split into separate LINK nodes.
        
    Behavior:
        - Identifies link syntax in the form `[link text](link_url)` within TEXT nodes.
        - Splits text before, between, and after link syntax into separate TEXT nodes.
        - Converts link syntax into LINK nodes with `link text` as the text and `link_url` as the URL.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            remaining_text = parts[1] if len(parts) > 1 else ""
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extract all markdown image syntax from a string.
    
    Args:
        text: A string potentially containing markdown image syntax in the form `![alt text](image_url)`.
    
    Returns:
        A list of tuples, where each tuple contains:
            - The `alt text` of the image.
            - The `image_url` of the image.
            
    Example:
        Input: "Here is an image ![example](http://example.com/image.png)"
        Output: [("example", "http://example.com/image.png")]
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extract all markdown link syntax from a string.
    
    Args:
        text: A string potentially containing markdown link syntax in the form `[link text](link_url)`.
    
    Returns:
        A list of tuples, where each tuple contains:
            - The `link text` of the link.
            - The `link_url` of the link.
            
    Example:
        Input: "Click [here](http://example.com) to visit the site."
        Output: [("here", "http://example.com")]
        
    Notes:
        - Does not extract image syntax (`![alt text](image_url)`) due to the negative lookbehind `(?<!!)`.
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def text_to_textnodes(text:str)->List[TextNode]:
    """
    Convert markdown-like text into a list of TextNode objects.
    
    Args:
        text: The markdown-like string to process.
    
    Returns:
        A list of TextNode objects representing the parsed text.
    """

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


