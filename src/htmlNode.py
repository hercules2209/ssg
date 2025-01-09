from typing import List

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        html = ""
        for key, value in self.props.items():
            html += f'{key}="{value}" '
        return html

    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, "
                f"children={self.children}, props={self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value") 
        if self.tag is None:
            return self.value
            
        props_html = self.props_to_html().rstrip()
        if props_html:
            return f"<{self.tag} {props_html}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: dict = None):
        super().__init__(tag=tag, children=children, value=None, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        props_html = self.props_to_html().rstrip()
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        if props_html:
            return f"<{self.tag} {props_html}>{inner_html}</{self.tag}>"
        return f"<{self.tag}>{inner_html}</{self.tag}>"
