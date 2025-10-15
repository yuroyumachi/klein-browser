
from common import Document
from enum import Enum
import ast

class TokenType(Enum):
    FIELD = 0
    SELF_EXPLAINING = FIELD + 1
    EOF = SELF_EXPLAINING + 1

class Token:
    def __init__(self, token: str)-> None:
        self.token = token

    @property
    def type(self)-> TokenType:
        if self.token == "":
            return TokenType.EOF 

        if self.token in ("{", "}", ":", ";", ",", "\n"):
            return TokenType.SELF_EXPLAINING
        else:
            return TokenType.FIELD

class TokenState(Enum):
    SELECTORS = 0
    KEY = SELECTORS + 1
    COLON = KEY + 1
    VALUE = COLON + 1
    END_DECLARAION = VALUE + 1

class Lexer:
    def __init__(self, source: Document)-> None:
        self.source = source

    def tokenizing(self)-> str:
        self.source.skip_whitespace()

        buffer = ""
        quote_ch = ""
        while ch := self.source.getch():
            if ch in ("\"", "\'"):
                quote_ch = ch if quote_ch == "" else ""
            elif quote_ch:
                buffer += ch
            elif ch in ("{", "}", ":", ";", ",", "\n"):
                if buffer:
                    self.source.ungetch(ch)
                else:
                    buffer = ch
                return buffer
            elif ch.isspace():
                self.source.ungetch(ch)
                return buffer
            else:
                buffer += ch
        
        return buffer

    def next(self)-> Token:
        return Token(self.tokenizing())

class Parser:
    def __init__(self)-> None:
        self.reset()

    def reset(self)-> None:
        self.lexer: Lexer | None = None
        self.selectors: list[str] = []
        self.declarations: dict[str, str] = {}

    def feed(self, source: str)-> None:
        self.lexer = Lexer(Document(source))

        token: Token
        while token := self.lexer.next():
            pass

if __name__ == "__main__":
    src = """body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
        
    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 2em;
        background-color: #fdfdff;
        border-radius: 0.5em;
        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        div {
            margin: 0 auto;
            width: auto;
        }
    }"""
    parser = Parser()
    parser.feed(src)
