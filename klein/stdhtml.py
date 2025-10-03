import html.parser
from htmllib import HTMLNode, print_node_tree

class Parser(html.parser.HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.root = HTMLNode("", {}, [])
        self.node_stack: list[HTMLNode] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.node_stack.append(
            HTMLNode(
                tag,
                {x : "" if y is None else y for x, y in attrs},
                []
            )
        )
        return super().handle_starttag(tag, attrs)
    
    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.node_stack[-1].add_child(
            HTMLNode(
                tag,
                {x : "" if y is None else y for x, y in attrs},
                []
            )
        )
    
    def handle_endtag(self, tag: str) -> None:
        while node := self.node_stack.pop():
            self.node_stack[-1].add_child(node)
            if tag == node.tag or len(self.node_stack) < 1:
                break
    
    def handle_data(self, data: str) -> None:
        self.node_stack[-1].add_child(data)

    def handle_comment(self, data: str) -> None:
        self.node_stack[-1].add_child(data)

    def handle_decl(self, decl: str) -> None:
        self.node_stack[-1].add_child(decl)

    def get_root(self)-> HTMLNode:
        return self.root

if __name__ == "__main__":
    with open("example.html", "rt") as f:
        source = f.read()

    parser = Parser()
    parser.feed(source)

    t = parser.get_root()
    print_node_tree(t)
