from tkinter import ttk

from gui.TextPreviewPopup import TextPreviewPopup
from key_rings.key_ring import KeyRing


class PublicKeyRingTable:
    def __init__(self, root, frame, parent):
        self.frame = frame
        self.root = root
        self.parent = parent
        self.button_data = [
            ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "1,7"],
            ["2,1", "2,2", "2,3", "2,4", "2,5", "2,6", "2,7"],
            ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7"],
        ]
        self.create_table()

    @staticmethod
    def create_table_row_public_ring(key: KeyRing):
        return [key.timestamp, key.key_id, key.get_public_key_as_string(), key.email, key.algorithm, key.user_name, key.key_size]

    def create_table(self):
        table_frame = ttk.Frame(self.frame)
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
        self.parent.render()
