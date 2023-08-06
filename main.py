import tkinter as tk
from tkinter import ttk

from gui.FilePicker import FilePicker
from gui.GenerateKeyForm import GenerateKeyForm
from gui.PasswordConfirmForm import PasswordConfirmForm
from gui.TextPreviewPopup import TextPreviewPopup
from key_rings.private_key_ring import privateKeyRing
from key_rings.private_key_utils import remove_key, get_private_key_by_id
from rsa_util.rsa_util import export_public_to_file


class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenPGP")

        self.buttons = ["Generate keys", "Import key", "Send message", "Receive message"]

        self.labelToId = {}

        self.button_data = [
            ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "1,7"],
            ["2,1", "2,2", "2,3", "2,4", "2,5", "2,6", "2,7"],
            ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7"],
        ]

        self.render()

    def on_click(self, name):
        if name == "Generate keys":
            GenerateKeyForm(self.root, self)

    def create_buttons(self):
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack()

        for i, name in enumerate(self.buttons):
            button = ttk.Button(buttons_frame, text=name, command=lambda x=name: self.on_click(x))
            button.grid(row=0, column=i, padx=5, pady=5)

    @staticmethod
    def create_table_row(key):
        return [key.e, key.keyId, '***', '***', key.email, key.algorith, key.name, key.keySize]

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def render(self):
        self.clear_window()
        self.create_buttons()
        self.create_table()

    def delete_key(self, event):
        remove_key(get_private_key_by_id(self.labelToId[event.widget]))
        self.render()

    def show_d(self, event):
        key = get_private_key_by_id(self.labelToId[event.widget])
        PasswordConfirmForm(self.root, self, key.d, key, "D")

    def show_n(self, event):
        key = get_private_key_by_id(self.labelToId[event.widget])
        TextPreviewPopup(self.root, key.n, "N")

    def export_public(self, event):
        key = get_private_key_by_id(self.labelToId[event.widget])
        file_picker = FilePicker()
        export_public_to_file(file_picker.filename, key)

    def create_table(self):
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10)

        headline_label = ttk.Label(table_frame, text="Private keys")
        headline_label.grid(row=0, columnspan=10)

        columns = ['E', 'KeyId', 'D', 'N', 'Email', 'Algorithm', 'Name', 'Key size', 'Export public', 'Export private', 'Delete']

        for col_idx, col_name in enumerate(columns):
            col_label = ttk.Label(table_frame, text=col_name, borderwidth=1, relief="solid")
            col_label.grid(row=1, column=col_idx, sticky="nsew")

            self.root.grid_columnconfigure(col_idx, weight=1)

        for row_idx, ring in enumerate(privateKeyRing):
            for col_idx, cell_value in enumerate(self.create_table_row(ring)):
                cell_label = ttk.Label(table_frame, text=cell_value, borderwidth=1, relief="solid")
                cell_label.grid(row=row_idx + 2, column=col_idx, sticky="nsew")

                if columns[col_idx] == "D":
                    cell_label.bind("<Button-1>", self.show_d)
                    self.labelToId[cell_label] = ring.id

                if columns[col_idx] == "N":
                    cell_label.bind("<Button-1>", self.show_n)
                    self.labelToId[cell_label] = ring.id

            export_label = ttk.Label(table_frame, text='Export public', borderwidth=1, relief="solid")
            export_label.grid(row=row_idx + 2, column=8, sticky="nsew")
            export_label.bind("<Button-1>", self.export_public)
            self.labelToId[export_label] = ring.id

            export_private_label = ttk.Label(table_frame, text='Export private', borderwidth=1, relief="solid")
            export_private_label.grid(row=row_idx + 2, column=9, sticky="nsew")

            delete_label = ttk.Label(table_frame, text='Delete', borderwidth=1, relief="solid")
            delete_label.grid(row=row_idx + 2, column=10, sticky="nsew")
            delete_label.bind("<Button-1>", self.delete_key)

            self.labelToId[delete_label] = ring.id

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)


def main():
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
