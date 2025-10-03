
from common import Document

class Rule:
    def __init__(self, selector: str, declarations: dict[str, str]):
        self.selector = selector
        self.declarations = declarations

class Rulesets:
    def __init__(self)-> None:
        self.rulesets: set[Rule] = set()

    def add_rule(self, rule: Rule)-> None:
        self.rulesets.add(rule)

def tokenizing(source: Document)-> None:
    buffer: str = ""
    while (ch := source.getch()) != "":
        if ch == "\n":
            pass
        if ch.isspace():
            pass
        if ch in ("{", "}"):
            pass
        if ch == ":":
            pass
        if ch == ";":
            pass
