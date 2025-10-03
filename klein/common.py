
from collections.abc import Iterator

class Document:
    def __init__(self, content: str) -> None:
        self.content: Iterator[str] = iter(content)
        self.buffer: list[str] = []

    def getch(self)-> str:
        if self.buffer != []:
            return self.buffer.pop()

        try:
            return next(self.content)
        except StopIteration:
            return ""

    def ungetch(self, ch: str)-> None:
        self.buffer.append(ch)

    def peek(self)-> str:
        if self.buffer == []:
            ch = self.getch()
    
            if ch != "":
                self.ungetch(ch)
    
            return ch
    
        return self.buffer[-1]

    def skip_whitespace(self)-> None:
        while self.peek() and self.peek().isspace():
            self.getch()
