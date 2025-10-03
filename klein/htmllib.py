
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from common import Document

class HTMLTokenType(Enum):
    DATA = 0
    START_TAG = DATA + 1
    SELF_CLOSING_TAG = START_TAG + 1
    END_TAG = SELF_CLOSING_TAG + 1
    COMMENT = END_TAG + 1
    DECLARATION = COMMENT + 1
    ESCAPE = DECLARATION + 1
    DOC_EOF = ESCAPE + 1

def tokenizing(source: Document)-> str:
    buffer: str = ""
    while (ch := source.getch()) != "":
        if not buffer:
            buffer = ch
            continue

        if ch == "<":
            source.ungetch(ch)
            return buffer
        elif ch == ">":
            buffer += ch
            if buffer.startswith("<"):
                return buffer
        elif ch == "&":
            source.ungetch(ch)
            return buffer
        elif ch == ";":
            buffer += ch
            if buffer.startswith("&"):
                return buffer
        elif ch.isspace():
            if not buffer[-1].isspace():
                buffer += " "
        else:
            buffer += ch

    return buffer


def token_type(token: str)-> HTMLTokenType:
    if token == "":
        return HTMLTokenType.DOC_EOF

    if token.startswith("<!--"):
        return HTMLTokenType.COMMENT

    if token.endswith(">"):
        if token.startswith("<!"):
            return HTMLTokenType.DECLARATION
        if token.startswith("</"):
            return HTMLTokenType.END_TAG
        if token.startswith("<") and token.endswith("/>"):
            return HTMLTokenType.SELF_CLOSING_TAG

        if token.startswith("<"):
            return (HTMLTokenType.START_TAG
                if token[1:-1].strip() != ""
                else HTMLTokenType.DATA
                )

    if token.startswith("&") and token.endswith(";"):
        return HTMLTokenType.ESCAPE
    
    return HTMLTokenType.DATA

class HTMLNode:
    def __init__(self, tag: str, attrs: dict[str, str] = {}, children: list[HTMLNode | str] = [])-> None:
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def add_child(self, child: HTMLNode | str)-> None:
        self.children.append(child)

def parse_attr_str(attr_str: str)-> dict[str, str]:
    key: str = ""
    attrs: dict[str, str] = {}
    buffer: str = ""
    quote_ch: str = ""
    for ch in attr_str:
        pass
        if quote_ch != "":
            if ch in ("\"", "\'"):
                quote_ch = ""
            else:
                buffer += ch
            continue

        if ch in ("\"", "\'"):
            quote_ch = ch
        elif ch == "=":
            key = buffer
            buffer = ""

        elif ch.isspace():
            if key == "":
                attrs[buffer] = ""
                key = ""
            else:
                attrs[key] = buffer
            buffer = ""
        else:
            buffer += ch

    if buffer or key:
        if key:
            attrs[key] = buffer
        else:
            attrs[buffer] = "" 
    
    return attrs

def parse_tag(content: str)-> tuple[str, dict[str, str]]:
    """take a start tag or self-closing tag, and it didn't wrap by any "<>"."""
    parts = content.split(None, 1)
    match parts:
        case [tag]:
            return tag, {}
        case [tag, attrs]:
            return tag, parse_attr_str(attrs)
        case _:
            return content, {}

def escape(entity: str)-> str:
    """take a escape entity to translate it."""
    entity_map: dict[str, str] = {
        "&nbsp;" : " ",
        "&lt;" : "<",
        "&gt;" : ">",
        "&amp;" : "&",
        "&quot;" : "\"",
        "&apos" : "\'",
        "&cent;" : "￠",
        "&pound;" : "£",
        "&yen;" : "¥",
        "&euro;" : "€",
        "&sect;" : "§",
        "&copy;" : "©",
        "&reg;" : "®",
        "&trade;" : "™",
        "&times;" : "×",
        "&divide;" : "÷"
    }
    if entity in entity_map:
        return entity_map[entity]
    if entity.startswith("&#"):
        try:
            ch = chr(int(entity[2:-1]))
        except:
            return entity

    return entity

def parse_end_tag(tag: str)-> str:
    tag, *_ = tag.split(None, 1)
    return tag

def build_node_tree(source: Document)-> HTMLNode:
    root = HTMLNode("", {}, [])
    node_stack: list[HTMLNode] = [root]

    while token := tokenizing(source):
        type_ = token_type(token)
        if type_ == HTMLTokenType.START_TAG:
            tag, attrs = parse_tag(token[1:-1])
            node_stack.append(HTMLNode(tag, attrs, []))
        
        if type_ == HTMLTokenType.SELF_CLOSING_TAG:
            tag, attrs = parse_tag(token[1:-2])
            node_stack[-1].add_child(HTMLNode(tag, attrs, []))

        if type_ == HTMLTokenType.END_TAG:
            tag = parse_end_tag(token[2:-1])
            while tag != node_stack[-1].tag and len(node_stack) > 1:
                node = node_stack.pop()
                node_stack[-1].add_child(node)

        if type_ == HTMLTokenType.DECLARATION:
            node_stack[-1].add_child(token)

        if type_ == HTMLTokenType.COMMENT:
            node_stack[-1].add_child(token)

        if type_ == HTMLTokenType.DATA:
            node_stack[-1].add_child(token)

        if type_ == HTMLTokenType.DOC_EOF:
            n = len(node_stack) - 1
            while n > 0:
                node_stack[n - 1].add_child(node_stack.pop())
                n -= 1
            break

    return root

def print_node_tree(node: HTMLNode, depth: int = 0)-> None:
    print("\t" * depth, end="")
    print(f":{'?' if node.children == [] else ''}{node.tag}, {node.attrs}:")
    buffer = ""
    k = 0
    for child in node.children:
        if isinstance(child, str):
            print("\t" * depth, end="")
            print(k, child)
            k += 1
        else:
            print_node_tree(child, depth + 1)

if __name__ == "__main__":
    with open("example.html", "rt") as f:
        source = f.read()

    s = Document(source)
    t = build_node_tree(s)
    print_node_tree(t)
