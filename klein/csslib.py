
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
    while (ch := source.getch()) != "":
        if ch == "\n":
            return buffer
        if ch.isspace():
            return buffer
        if ch in ("{", "}", ":", ";"):
            if buffer:
                return buffer
            return ch

    return ""


class TokenState(Enum):
    SELECTOR = 0
    OPEN_BRACE = SELECTOR + 1
    KEY = OPEN_BRACE + 1
    COLON = KEY + 1
    VALUE = COLON + 1
    END_RULE = VALUE + 1
    CLOSE_BRACE = END_RULE

def make_rule(source: Document)-> Rules:
    selectors: list[str] = []
    declaration_pair: tuple[str, str] = ("", "")
    declarations: dict[str, str] = {}

    state: TokenState = TokenState.SELECTOR
    while (token := Token(tokenizing(source))).type != TokenType.EOF:
        if state == TokenState.SELECTOR:
            if token.type == TokenType.FIELD:
                selectors.append(token.token)
                state = TokenState.OPEN_BRACE

        if state == TokenState.OPEN_BRACE:
            if token.type == TokenType.OPEN_BRACE:
                state = TokenState.KEY
            elif token.type == TokenType.FIELD and len(selectors) < 3:
                selectors.append(token.token)
            elif token.type == TokenType.FIELD and len(selectors) >= 3:
                selectors.clear()
                state = TokenState.SELECTOR

        if state == TokenState.KEY:
            if token.type == TokenType.FIELD:
                pass

    return Rules(selectors, declarations)
