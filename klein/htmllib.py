
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
    ch: str = ""
    while ch := source.getch():
        match ch:        
            case '<':
                case

class HTMLNode:
    def __init__(self)-> None:
        pass
