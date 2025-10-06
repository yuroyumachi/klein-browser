
from common import Document
from enum import Enum

class Rules:
    def __init__(self, selector: list[str], declarations: dict[str, str]):
        self.selector = selector
        self.declarations = declarations

class Ruleset:
    def __init__(self)-> None:
        self.rulesets: set[Rules] = set()

    def add_rule(self, rule: Rules)-> None:
        self.rulesets.add(rule)

class TokenType(Enum):
    FIELD = 0
    OPEN_BRACE = FIELD + 1
    CLOSE_BRACE = OPEN_BRACE + 1
    COLON = CLOSE_BRACE + 1
    SEMICOLON = COLON + 1
    WHITESPACE = SEMICOLON + 1
    NEWLINE = WHITESPACE + 1
    EOF = NEWLINE + 1

class Token:
    def __init__(self, token: str)-> None:
        self.token = token

    @property
    def type(self)-> TokenType:
        if self.token == "":
            return TokenType.EOF 
        if self.token == "{":
            return TokenType.OPEN_BRACE
        elif self.token == "}":
            return TokenType.CLOSE_BRACE
        elif self.token == ":":
            return TokenType.COLON
        elif self.token == ";":
            return TokenType.SEMICOLON
        elif self.token == "\n":
            return TokenType.NEWLINE
        elif self.token.isspace():
            return TokenType.WHITESPACE
        else:
            return TokenType.FIELD

def tokenizing(source: Document)-> str:
    buffer: str = ""
    while ch := source.getch():
        if ch == "\n":
            if buffer:
                source.ungetch(ch)
                return buffer
            return ch
        elif ch.isspace():
            if buffer:
                source.ungetch(ch)
                return buffer
            return ch
        elif ch in ("{", "}", ":", ";"):
            if buffer:
                source.ungetch(ch)
                return buffer
            return ch
        else:
            buffer += ch

    return ""

class ExpectToken(Enum):
    SELECTOR = 0
    OPEN_BRACE = SELECTOR + 1
    KEY = OPEN_BRACE + 1
    COLON = KEY + 1
    VALUE = COLON + 1
    END_RULE = VALUE + 1
    CLOSE_BRACE = END_RULE

def make_rule(source: Document)-> Rules:
    selectors: list[str] = []
    key: str = ""
    declarations: dict[str, str] = {}

    state: ExpectToken = ExpectToken.SELECTOR

    while (token := Token(tokenizing(source))).type != TokenType.EOF:
        if state == ExpectToken.SELECTOR:
            if token.type == TokenType.FIELD:
                selectors.append(token.token)
                state = ExpectToken.OPEN_BRACE

        if state == ExpectToken.OPEN_BRACE:
            if token.type == TokenType.OPEN_BRACE:
                state = ExpectToken.KEY
            elif token.type == TokenType.FIELD and len(selectors) < 3:
                selectors.append(token.token)
            elif token.type == TokenType.FIELD and len(selectors) >= 3:
                selectors.clear()
                state = ExpectToken.SELECTOR

        if state == ExpectToken.KEY:
            if token.type == TokenType.FIELD:
                key = token.token
                state = ExpectToken.COLON
                                    
        if state == ExpectToken.COLON:
            if token.type == TokenType.COLON:
                state = ExpectToken.VALUE
            if token.type == TokenType.SEMICOLON:
                declarations[key] = ""
                state = ExpectToken.CLOSE_BRACE

        if state == ExpectToken.VALUE:
            if token.type == TokenType.FIELD:
                declarations[key] = token.token
            if token.type == TokenType.SEMICOLON:
                state = ExpectToken.CLOSE_BRACE

        if state == ExpectToken.END_RULE:
            if token.type == TokenType.SEMICOLON:
                state = ExpectToken.SELECTOR
            elif token.type == TokenType.CLOSE_BRACE:
                state = ExpectToken.SELECTOR

    return Rules(selectors, declarations)

if __name__ == "__main__":
    doc = Document("body { color: red; }")
    rule = make_rule(doc)
    print(rule.selector)
    print(rule.declarations)
