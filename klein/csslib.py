
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
    def __init__(self, source: str)-> None:
        self.state: LexerState | None = None

        self.preprocessing(source)

    def preprocessing(self, source: str)-> None:
        buffer: str = ""
        
        i = 0
        j = 0
        n = len(source)
        commented: bool = False
        while i < n:
            ch = source[i]
            if ch == "/" and source[i+1] == "*":
                i += 2
                while i < n and source[i] != "*" and source[i+1] != "/":
                    i += 1
                else:
                    i += 2
            elif ch.isspace():
                if not buffer.endswith(" "):
                    buffer += " "
                i += 1
            else:
                buffer += ch
                i += 1

        self.source = buffer
        self.length = len(self.source)
        self.position = 0
        return

    def next(self)-> tuple[TokenType, str]:
        buffer: str = ""

        while self.position < self.length:
            if self.state is None:
                match self.source[self.position]:
                    case _ if self.source[self.position]:
                        self.state = LexerState.WHITESPACE_TOKEN
                    case "\"":
                        self.state = LexerState.STRING_TOKEN
                    case "#":
                        pass
                    case "\'":
                        self.state = LexerState.STRING_TOKEN
                    case "(" | ")" | "[" | "]" | "{" | "}":
                        return (TokenType.SELF_EXPLAINING, self.source[self.position])
                    case "+":
                        pass
                    case ",":
                        return (TokenType.COMMA, "")
                    case "-":
                        pass
                    case ".":
                        pass
                    case ":":
                        return (TokenType.COLON, "")
                    case ";":
                        return (TokenType.SEMICOLON, "")
                    case "<":
                        pass
                    case "@":
                        pass
                    case "\\":
                        pass
                    case x if x.isdigit():
                        self.state = LexerState.NUMBER_TOKEN
                    case x if x.isalpha() or x == "_":
                        self.state = LexerState.IDENT_TOKEN
                    case _:
                        return (TokenType.DELIM, self.source[self.position])
            elif self.state == LexerState.STRING_TOKEN:
                pass

            self.position += 1

class Parser:
    def __init__(self)-> None:
        self.reset()

    def reset(self)-> None:
        self.lexer: Lexer | None = None
        self.selectors: list[str] = []
        self.declarations: dict[str, str] = {}

    def feed(self, source: str)-> None:
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
    Lexer(src)
    # parser = Parser()
    # parser.feed(src)
