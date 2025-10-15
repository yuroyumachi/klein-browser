
from common import Document
from enum import Enum

class TokenType(Enum):
    IDENT            = 0
    FUNCTION         = IDENT            + 1
    AT_KEYWORD       = FUNCTION         + 1
    HASH             = AT_KEYWORD       + 1
    STRING           = HASH             + 1
    BAD_STRING_TOKEN = STRING           + 1
    URL              = BAD_STRING_TOKEN + 1
    BAD_URL          = URL              + 1
    DELIM            = BAD_URL          + 1
    NUMBER           = DELIM            + 1
    PERCENTAGE       = NUMBER           + 1
    DIMENSION        = PERCENTAGE       + 1
    WHITESPACE       = DIMENSION        + 1
    CDO              = WHITESPACE       + 1
    CDC              = CDO              + 1
    COLON            = CDC              + 1
    SEMICOLON        = COLON            + 1
    COMMA            = SEMICOLON        + 1
    SELF_EXPLAINING  = COMMA            + 1

class Token:
    def __init__(self, token: str)-> None:
        self.token = token

    @property
    def type(self)-> TokenType | None:
        if self.token == "":
            return None
        
        # WIP: return other TokenTypes

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

    def handle_selectors(self, selectors: list[str])-> None:
        pass

    def handle_declarations(self, declarations: dict[str, str])-> None:
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
