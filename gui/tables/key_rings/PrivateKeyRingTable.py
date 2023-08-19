from tkinter import ttk
from gui.dialogs.general.FolderPicker import FolderPicker
from gui.dialogs.general.TextPreviewPopup import TextPreviewPopup
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


class PrivateKeyRingTable:
    def __init__(self, root, frame, parent, email, key_rings):
        self.frame = frame
        self.root = root
        self.parent = parent
        self.button_data = [
            ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "1,7"],
            ["2,1", "2,2", "2,3", "2,4", "2,5", "2,6", "2,7"],
            ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7"],
        ]
        self.email = email
        self.key_rings = key_rings
        self.create_table()

    @staticmethod
    def create_table_row_private_ring(key: PrivateKeyRing):
        return [key.timestamp, key.key_id, key.public_key, key.encrypted_private_key,
                key.user_id]

    def create_table(self):
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=0, column=0)

        headline_label = ttk.Label(table_frame, text="Private keys ring")
        headline_label.grid(row=0, columnspan=10)

        columns = ['Timestamp', 'Key ID', 'Public Key', 'Encrypted Private Key', 'User ID', 'Actions']

        for col_idx, col_name in enumerate(columns):
            col_label = ttk.Label(table_frame, text=col_name, borderwidth=1, relief="solid", padding=5)
            col_label.grid(row=1, column=col_idx, sticky="nsew")

            self.root.grid_columnconfigure(col_idx, weight=1)

        for row_idx, ring in enumerate(self.key_rings):
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

            actions_frame = ttk.Frame(table_frame)
            actions_frame.grid(row=row_idx + 2, column=5, sticky="nsew")
            export_private_key_button = ttk.Button(actions_frame, text="Export Private Key",
                                                   command=lambda arg=ring: self.export_private_ring(arg))
            export_public_key_button = ttk.Button(actions_frame, text="Export Public Key",
                                                  command=lambda arg=ring: self.export_public_ring(arg))
            delete_key_ring_button = ttk.Button(actions_frame, text="Delete Key Ring",
                                                command=lambda arg=ring: self.delete_from_table(arg))
            export_private_key_button.grid(row=0, column=0)
            export_public_key_button.grid(row=0, column=1)
            delete_key_ring_button.grid(row=0, column=2)

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)

    def clear_window(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def render(self):
        self.clear_window()
        self.create_table()

    def delete_from_table(self, ring):
        PrivateKeyRing.delete_row(self.email, ring)
        self.render()

    @staticmethod
    def export_private_ring(ring: PrivateKeyRing):
        file_picker = FolderPicker()
        ring.export_private_key(file_picker.directory)

    @staticmethod
    def export_public_ring(ring: PrivateKeyRing):
        file_picker = FolderPicker()
        ring.export_public_key(file_picker.directory)
