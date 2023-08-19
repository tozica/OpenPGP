import tkinter.constants
from tkinter import ttk

from gui.dialogs.GenerateKeyForm import GenerateKeyForm
from gui.tables.user.UserListTable import UserListTable


class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenPGP")
        self.buttons = ["Generate keys"]
        self.render()

    def on_click(self, name):
        if name == "Generate keys":
            GenerateKeyForm(self.root, self)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_buttons(self):
        buttons_frame = ttk.Frame(self.root, width=500, height=1000)
        buttons_frame.pack(side=tkinter.TOP)

        for i, name in enumerate(self.buttons):
            button = ttk.Button(buttons_frame, text=name, command=lambda x=name: self.on_click(x))
            button.grid(row=0, column=i, padx=5, pady=5)

    def create_tables(self):
        table_frame = ttk.Frame(self.root, width=1000, height=1000)
        table_frame.pack(side=tkinter.BOTTOM, pady=10)
        UserListTable(self.root, table_frame, self)

    def render(self):
        self.clear_window()
        self.create_buttons()
        self.create_tables()
