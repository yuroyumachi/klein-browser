
from common import Document
from enum import Enum

class Rules:
    def __init__(self, selector: str, declarations: dict[str, str]):
        self.selector = selector
        self.declarations = declarations

class Ruleset:
    def __init__(self)-> None:
        self.rulesets: set[Rules] = set()

    def add_rule(self, rule: Rules)-> None:
        self.rulesets.add(rule)

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

class TokenType(Enum):
    FIELD = 0
    OPEN_BRACE = FIELD + 1
    CLOSE_BRACE = OPEN_BRACE + 1
    COLON = CLOSE_BRACE + 1
    SEMICOLON = COLON + 1
    WHITESPACE = SEMICOLON + 1
    NEWLINE = WHITESPACE + 1
    EOF = NEWLINE + 1

def token_type(token: str)-> TokenType:
    if token == "":
        return TokenType.EOF 
    if token == "{":
        return TokenType.OPEN_BRACE
    elif token == "}":
        return TokenType.CLOSE_BRACE
    elif token == ":":
        return TokenType.COLON
    elif token == ";":
        return TokenType.SEMICOLON
    elif token == "\n":
        return TokenType.NEWLINE
    elif token.isspace():
        return TokenType.WHITESPACE
    else:
        return TokenType.FIELD

def make_rule(source: Document)-> Rules:

    selector: str = tokenizing(source)
    while token_type(selector) != TokenType.FIELD:
        selector = tokenizing(source)

    declarations: dict[str, str] = {}

    property: str = ""
    value: str = ""

    return Rules(selector, declarations)
