
from klein import HTMLViewer, StatusBar, HorizontalRule
from tkinter import Tk, Frame, Button, Label, Entry
from tkinter.ttk import Frame, Button, Label, Entry, Style

class App(Tk):
    def __init__(self, *cnf, **kw)-> None:
        super().__init__(*cnf, **kw)

        self.title("Klein")
        self.geometry("400x300")

        self.style = Style(self)
        self.style.configure("TButton", width=4)

        self.panel_frame = Frame(self)
        self.panel_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.panel_frame.grid_rowconfigure(1, weight=1)
        self.panel_frame.grid_columnconfigure(0, weight=1)

        self.url_bar_frame = Frame(self.panel_frame)
        self.url_bar_frame.grid(row=0, column=0, sticky="NSEW")
        self.backward_botton = Button(self.url_bar_frame, text="<")
        self.backward_botton.pack(side="left")
        self.refresh_botton = Button(self.url_bar_frame, text="R")
        self.refresh_botton.pack(side="left")
        self.url_entry = Entry(self.url_bar_frame)
        self.url_entry.pack(side="left", expand=True, fill="both")
        self.goto_button = Button(self.url_bar_frame, text=">>")
        self.goto_button.pack(side="left")

        print(self.style.element_options(self.goto_button))

        self.viewer = HTMLViewer(self.panel_frame)
        self.viewer.grid(row=1, column=0, sticky="NSEW")

        HorizontalRule(self.panel_frame).grid(row=2, column=0, sticky="NSEW")

        self.title_bar = StatusBar(self.panel_frame, status_text="Hello World! And World Wide Web!")
        self.title_bar.grid(row=3, column=0, sticky="NSEW")

        self.action_info_bar = StatusBar(self.panel_frame, relief="raised", borderwidth=1)
        self.action_info_bar.grid(row=5, column=0, sticky="NSEW")

    def run(self)-> None:
        self.mainloop()

if __name__ == "__main__":
    App().run()
