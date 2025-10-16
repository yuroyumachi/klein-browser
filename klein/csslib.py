
from common import Document
from enum import Enum, auto

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

class LexerState(Enum):
    COMMENT          = auto()
    HEX_DIGIT        = auto()
    ESCAPE           = auto()
    WHITESPACE_TOKEN = auto()
    WS               = auto()
    IDENT_TOKEN      = auto()
    FUNCTION_TOKEN   = auto()
    AT_KEYWORD_TOKEN = auto()
    HASH_TOKEN       = auto()
    STRING_TOKEN     = auto()
    URL_TOKEN        = auto()
    NUMBER_TOKEN     = auto()
    DIMENSION_TOKEN  = auto()
    PERCNETAGE_TOKEN = auto()
    CDO_TOKEN        = auto()
    CDC_TOKEN        = auto()

class Lexer:
    def __init__(self, source: Document)-> None:
        self.source = source
        self.state: LexerState | None = None

    def tokenizing(self)-> str:
        buffer: str = ""

        ch: str = ""
        match ch := self.source.getch():
            case "/" if self.source.peek() == "*":
                while ch := self.source.getch():
                    if ch == "*" and self.source.peek() == "/":
                        break

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
