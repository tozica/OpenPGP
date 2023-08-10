from tkinter import ttk

from gui.dialogs.FilePicker import FilePicker
from gui.dialogs.TextPreviewPopup import TextPreviewPopup
from key_rings.key_ring import KeyRing


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
    def create_table_row_private_ring(key: KeyRing):
        return [key.timestamp, key.key_id, key.get_public_key_as_string(), key.get_private_key_as_string(),
                key.email, key.algorithm, key.user_name, key.key_size]

    def create_table(self):
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=0, column=0)

        headline_label = ttk.Label(table_frame, text="Private keys ring")
        headline_label.grid(row=0, columnspan=10)

        columns = ['Timestamp', 'Key ID', 'Public Key', 'Encrypted Private Key', 'User ID', 'Algorithm',
                   'User Name', 'Key Size', 'Export private', 'Delete']

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

            export_label = ttk.Label(table_frame, text='Export private', borderwidth=1, relief="solid")
            export_label.grid(row=row_idx + 2, column=8, sticky="nsew")
            export_label.bind("<Button-1>", lambda event, arg=ring: self.export_private_ring(ring))

            delete_label = ttk.Label(table_frame, text='Delete', borderwidth=1, relief="solid")
            delete_label.grid(row=row_idx + 2, column=10, sticky="nsew")
            delete_label.bind("<Button-1>", lambda event, arg=ring: self.delete_from_table(ring))

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)

    def clear_window(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def render(self):
        self.clear_window()
        self.create_table()

    def delete_from_table(self, ring):
        KeyRing.private_key_ring_by_user[self.email].remove(ring)
        self.render()

    @staticmethod
    def export_private_ring(ring: KeyRing):
        file_picker = FilePicker()
        ring.export_private_key(file_picker.directory)

