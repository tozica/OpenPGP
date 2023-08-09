import tkinter.constants
from tkinter import ttk

from gui.FilePicker import FilePicker
from gui.GenerateKeyForm import GenerateKeyForm
from gui.TextPreviewPopup import TextPreviewPopup
from key_rings.key_ring import KeyRing


class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenPGP")
        self.buttons = ["Generate keys", "Import key", "Send message", "Receive message"]
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
        buttons_frame = ttk.Frame(self.root, width=500, height=1000)
        buttons_frame.pack(side=tkinter.TOP)

        for i, name in enumerate(self.buttons):
            button = ttk.Button(buttons_frame, text=name, command=lambda x=name: self.on_click(x))
            button.grid(row=0, column=i, padx=5, pady=5)

    @staticmethod
    def create_table_row_private_ring(key: KeyRing):
        return [key.timestamp, key.key_id, key.get_public_key_as_string(), key.get_private_key_as_string(), key.email, key.algorithm, key.user_name, key.key_size]

    @staticmethod
    def create_table_row_public_ring(key: KeyRing):
        return [key.timestamp, key.key_id, key.get_public_key_as_string(), key.email, key.algorithm, key.user_name, key.key_size]

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_tables(self):
        table_frame = ttk.Frame(self.root, width=1000, height=1000)
        table_frame.pack(side=tkinter.BOTTOM, pady=10)
        self.create_private_ring_table(table_frame)
        self.create_public_ring_table(table_frame)

    def create_private_ring_table(self, frame):
        table_frame = ttk.Frame(frame)
        table_frame.grid(row=0, column=0)

        headline_label = ttk.Label(table_frame, text="Private keys ring")
        headline_label.grid(row=0, columnspan=10)

        columns = ['Timestamp', 'Key ID', 'Public Key', 'Encrypted Private Key', 'User ID', 'Algorithm',
                   'User Name', 'Key Size', 'Export private', 'Delete']

        for col_idx, col_name in enumerate(columns):
            col_label = ttk.Label(table_frame, text=col_name, borderwidth=1, relief="solid", padding=5)
            col_label.grid(row=1, column=col_idx, sticky="nsew")

            self.root.grid_columnconfigure(col_idx, weight=1)

        for row_idx, ring in enumerate(KeyRing.key_rings):
            for col_idx, cell_value in enumerate(self.create_table_row_private_ring(ring)):
                cell_label = ttk.Label(table_frame, text=str(cell_value)[:20], borderwidth=1, relief="solid", padding=5)
                cell_label.grid(row=row_idx + 2, column=col_idx, sticky="nsew")

                if columns[col_idx] == "Public Key":
                    cell_label.bind("<Button-1>",
                                    lambda event, arg=ring:
                                    TextPreviewPopup(self.root, ring.get_public_key_as_string(), "N"))

                if columns[col_idx] == "Encrypted Private Key":
                    cell_label.bind("<Button-1>",
                                    lambda event, arg=ring:
                                    TextPreviewPopup(self.root, ring.get_private_key_as_string(), "N"))

            export_label = ttk.Label(table_frame, text='Export private', borderwidth=1, relief="solid")
            export_label.grid(row=row_idx + 2, column=8, sticky="nsew")
            export_label.bind("<Button-1>", ring.export_private_key)

            delete_label = ttk.Label(table_frame, text='Delete', borderwidth=1, relief="solid")
            delete_label.grid(row=row_idx + 2, column=10, sticky="nsew")
            delete_label.bind("<Button-1>", lambda event, arg=ring: self.delete_from_table(ring))

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)

    def create_public_ring_table(self, frame):
        table_frame = ttk.Frame(frame)
        table_frame.grid(row=1, column=0)

        headline_label = ttk.Label(table_frame, text="Public keys ring")
        headline_label.grid(row=0, columnspan=10)

        columns = ['Timestamp', 'Key ID', 'Public Key', 'User ID', 'Algorithm',
                   'User Name', 'Key Size', 'Export private', 'Delete']

        for col_idx, col_name in enumerate(columns):
            col_label = ttk.Label(table_frame, text=col_name, borderwidth=1, relief="solid", padding=5)
            col_label.grid(row=1, column=col_idx, sticky="nsew")

            self.root.grid_columnconfigure(col_idx, weight=1)

        for row_idx, ring in enumerate(KeyRing.key_rings):
            for col_idx, cell_value in enumerate(self.create_table_row_public_ring(ring)):
                cell_label = ttk.Label(table_frame, text=str(cell_value)[:20], borderwidth=1, relief="solid", padding=5)
                cell_label.grid(row=row_idx + 2, column=col_idx, sticky="nsew")

                if columns[col_idx] == "Public Key":
                    cell_label.bind("<Button-1>",
                                    lambda event, arg=ring:
                                    TextPreviewPopup(self.root, ring.get_public_key_as_string(), "N"))

            export_label = ttk.Label(table_frame, text='Export public', borderwidth=1, relief="solid")
            export_label.grid(row=row_idx + 2, column=8, sticky="nsew")
            export_label.bind("<Button-1>", ring.export_public_key)

            delete_label = ttk.Label(table_frame, text='Delete', borderwidth=1, relief="solid")
            delete_label.grid(row=row_idx + 2, column=10, sticky="nsew")
            delete_label.bind("<Button-1>", lambda event, arg=ring: self.delete_from_table(ring))

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)

    def delete_from_table(self, ring):
        KeyRing.key_rings.remove(ring)
        self.render()

    def render(self):
        self.clear_window()
        self.create_buttons()
        self.create_tables()
