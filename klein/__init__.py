
from tkinter import Frame, Label, StringVar

class HTMLViewer(Frame):
    def __init__(self, *cnf, **kw)-> None:
        super().__init__(*cnf, **kw)

class HorizontalRule(Frame):
    def __init__(self, master = None, width: int = 1, background: str = "#000000", *cnf, **kw)-> None:
        super().__init__(master, height=width, background=background, *cnf, **kw)

class StatusBar(Frame):
    def __init__(self, master, status_text: str = ":STATUS:", *cnf, **kw)-> None:
        super().__init__(master, *cnf, **kw)

        background = None
        if "background" in kw:
            background = kw["background"]
        elif "bg" in kw:
            background = kw["bg"]

        self.status_value = StringVar(self, status_text)
        self.status_label = Label(self, textvariable=self.status_value)
        self.status_label.grid(row=0, column=0)

    def set_status(self, value: str)-> None:
        self.status_text = value
        self.status_value.set(self.status_text)
