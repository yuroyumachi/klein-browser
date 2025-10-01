
from __future__ import annotations
from collections.abc import Iterator
from enum import Enum
from dataclasses import dataclass

class HTMLTokenType(Enum):
    DATA = 0
    START_TAG = DATA + 1
    SELF_CLOSING_TAG = START_TAG + 1
    END_TAG = SELF_CLOSING_TAG + 1
    COMMENT = END_TAG + 1
    DECLARATION = COMMENT + 1
    ESCAPE = DECLARATION + 1
    DOC_EOF = ESCAPE + 1

class Document:
    def __init__(self, content: str) -> None:
        self.content: Iterator[str] = iter(content)
        self.buffer: list[str] = []

    def getch(self)-> str:
        if self.buffer != []:
            return self.buffer.pop()

        try:
            return next(self.content)
        except StopIteration:
            return ""

    def ungetch(self, ch: str)-> None:
        self.buffer.append(ch)

    def peek(self)-> str:
        if self.buffer == []:
            ch = self.getch()
    
            if ch != "":
                self.ungetch(ch)
    
            return ch
    
        return self.buffer[-1]

    def skip_whitespace(self)-> None:
        while self.peek() and self.peek().isspace():
            self.getch()

@dataclass
class HTMLToken:
    type: HTMLTokenType
    content: str

def tokenizing(source: Document)-> HTMLToken:
    buffer: str = ""

    while (ch := source.getch()) != "":
        if buffer == "":
            buffer += ch
            continue

        if buffer.startswith("<!--"):
            while (ch := source.getch()) != "":
                if buffer.endswith("-->"):
                    return HTMLToken(HTMLTokenType.COMMENT, buffer)
            return HTMLToken(HTMLTokenType.COMMENT, buffer)

        match ch:
            case "<":
                source.ungetch(ch)
                return HTMLToken(HTMLTokenType.DATA, buffer)

            case ">":
                buffer += ch
                
                if not buffer.startswith("<"):
                    continue

                if buffer.startswith("<!"):
                    return HTMLToken(HTMLTokenType.DECLARATION, buffer)
                elif buffer.startswith("</"):
                    return HTMLToken(HTMLTokenType.END_TAG, buffer)
                elif buffer.endswith("/>"):
                    return HTMLToken(HTMLTokenType.SELF_CLOSING_TAG, buffer)
                elif buffer.startswith("<"):
                    return HTMLToken(HTMLTokenType.START_TAG, buffer)

            case "&":
                source.ungetch(ch)
                return HTMLToken(HTMLTokenType.DATA, buffer)
            
            case ";":
                buffer += ch

                if buffer.startswith("&"):
                    return HTMLToken(HTMLTokenType.ESCAPE, buffer)

            case _ if ch.isspace():
                if not buffer[-1].isspace():
                    buffer += ch

            case _:
                buffer += ch

    if buffer == "":
        return HTMLToken(HTMLTokenType.DOC_EOF, buffer)

    return HTMLToken(HTMLTokenType.DATA, buffer)

class HTMLNode:
    def __init__(self, tag: str, attr: dict[str, str] = {}, child: list[HTMLNode] = [])-> None:
        self.tag = tag
        self.attr = attr
        self.child = child

def parse_attr_str(attr_str: str)-> dict[str, str]:
    key: str = ""
    attrs: dict[str, str] = {}
    buffer: str = ""
    quote_ch: str = ""
    for ch in attr_str:
        if quote_ch != "":
            if ch in ("\"", "\'"):
                quote_ch = ""
            else:
                buffer += ch

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
    
    return attrs

def parse_tag(token: HTMLToken)-> tuple[str, dict[str, str]]:
    if token.type == HTMLTokenType.START_TAG:
        content = token.content[1:-1]
    else:
        content = token.content[1:-2]

    tag, attr_str = content.split(None, 1)

    attr_pair: list[str] = []
    attrs: dict[str, str] = parse_attr_str(attr_str)

    return (tag, attrs)

def escape(entity: HTMLToken)-> str:
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
    if entity.content in entity_map:
        return entity_map[entity.content]
    if entity.content.startswith("&#"):
        try:
            ch = chr(int(entity.content[2:-1]))
        except:
            return entity.content

    return entity.content

def parse_end_tag(token: HTMLToken)-> str:
    content = token.content[2:-1]
    tag, _ = content.split(None, 1)
    return tag

def build_node_tree(source: Document)-> None:
    pass

if __name__ == "__main__":
    with open("example.html", "rt") as f:
        source = f.read()

    s = Document(source)
    while token := tokenizing(s):
        if token.type == HTMLTokenType.DOC_EOF:
            break
        print(f"{token.type}, {token.content}")
