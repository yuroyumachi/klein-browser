
from common import Document
from enum import Enum

class Declaration:
    def __init__(self, property: str, value: str, important: bool)-> None:
        self.property = property
        self.value = value
        self.important = important

class Rule:
    def __init__(self, selectors: list[str], declarations: list[Declaration])-> None:
        self.selectors = selectors
        self.declarations = declarations

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

def tokenizing(source: Document)-> str:
    buffer: str = ""
    quote_ch: str = ""
    in_comment: bool = False
    while ch := source.getch():
        if in_comment:
            if ch == "*" and source.getch() == "/":
                in_comment = False
        
        elif quote_ch and ch == quote_ch:
            quote_ch = ""
            return buffer
        
        elif quote_ch:
            buffer += ch
            continue
        
        elif ch in ("\"", "\'"):
            quote_ch = ch
        
        elif ch.isspace():
            if buffer:
                return buffer
            source.skip_whitespace()
            return " "
        
        elif ch in ("{", "}", ":", ";", ",", "\n"):
            if buffer:
                source.ungetch(ch)
                return buffer
            return ch
        
        elif ch == "/":
            if buffer:
                source.ungetch(ch)
                return buffer
            if source.peek() == "*":
                in_comment = True
        
        else:
            buffer += ch

    return buffer

class TokenState(Enum):
    SELECTORS = 0
    KEY = SELECTORS + 1
    COLON = KEY + 1
    VALUE = COLON + 1
    END_DECLARAION = VALUE + 1

def make_rule(source: Document)-> list[Rule]:
    rule = Rule([], [])
    selectors: list[str] = []
    declarations: list[Declaration] = []
    key = ""

    state: TokenState = TokenState.SELECTORS
    while token := Token(tokenizing(source)):
        if token.type == TokenType.EOF:
            break
        if state == TokenState.SELECTORS:
            if token.token == "{":
                state = TokenState.KEY
                continue
            elif token.type == TokenType.FIELD:
                selectors.append(token.token)
        elif state == TokenState.KEY:
            if token.token == "}":
                break

if __name__ == "__main__":
    doc = Document("""body {
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
    }""")
    rule = make_rule(doc)
    print(rule.selector)
    print(rule.declarations)
