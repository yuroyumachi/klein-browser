
from common import Document
from enum import Enum

class Declaration:
    def __init__(self, property: str, value: str, important: bool)-> None:
        self.property = property
        self.value = value
        self.important = important

    def __repr__(self) -> str:
        return f""":\
property>> {self.property},
value>> {self.value},
important>> {self.important}
:"""

class Rule:
    def __init__(self, selectors: list[str], declarations: list[Declaration])-> None:
        self.selectors = selectors
        self.declarations = declarations
    
    def __repr__(self) -> str:
        selectors = ", ".join(self.selectors)
        return f":selectors>> {self.selectors}::declarations>> {self.declarations}:"

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
        self.lexer = Lexer(Document(""))
        self.tree = {}

    def feed(self, source: Document)-> None:
        self.lexer.source = source
        while token := self.lexer.next():
            if token.type == TokenType.EOF:
                print(token.token)
                break
            else:
                print(token.token)
                self.parse_field(token)

    def parse_field(self, token: Token)-> None:
        state = TokenState.SELECTORS
        selectors = []
        declarations = []
        property = ""
        value = ""
        important = False

        while token := self.lexer.next():
            if token.type == TokenType.EOF:
                break
            elif token.type == TokenType.SELF_EXPLAINING:
                if state == TokenState.SELECTORS:
                    state = TokenState.KEY
                elif state == TokenState.KEY:
                    state = TokenState.COLON
                elif state == TokenState.COLON:
                    state = TokenState.VALUE
                elif state == TokenState.VALUE:
                    state = TokenState.END_DECLARAION
            elif token.type == TokenType.FIELD:
                if state == TokenState.SELECTORS:
                    selectors.append(token.token)
                elif state == TokenState.KEY:
                    property = token.token
                    state = TokenState.COLON
                elif state == TokenState.COLON:
                    state = TokenState.VALUE
                elif state == TokenState.VALUE:
                    value += token.token
                elif state == TokenState.END_DECLARAION:
                    if token.token == "!important":
                        important = True
                    else:
                        declarations.append(Declaration(property, value, important))
                        property = ""
                        value = ""
                        important = False
                        state = TokenState.KEY

        if property and value:
            declarations.append(Declaration(property, value, important))

        # if selectors and declarations:
        rule = Rule(selectors, declarations)
        print(rule)

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
    parser = Parser()
    parser.feed(doc)
