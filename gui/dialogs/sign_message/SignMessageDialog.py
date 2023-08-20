import tkinter as tk
from tkinter import ttk, TOP, RIGHT, BOTTOM, LEFT

from gui.dialogs.general.TextPreviewPopup import TextPreviewPopup
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


class SignMessageDialog:
    def __init__(self, root, parent, email, ring):
        self.root = root
        self.parent = parent
        self.email = email
        self.ring = ring
        self.key_rings = (
            PrivateKeyRing.private_key_ring_by_user)[email] if email in PrivateKeyRing.private_key_ring_by_user else []
        self.button_data = [
            ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "1,7"],
            ["2,1", "2,2", "2,3", "2,4", "2,5", "2,6", "2,7"],
            ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7"],
        ]
        self.send_message_dialog = tk.Toplevel(self.root)
        self.send_message_dialog.title("Select private key")
        self.dialog_frame = ttk.Frame(self.send_message_dialog)
        self.dialog_frame.pack(fill="both", expand=True)
        self.create_table()
    pass

    @staticmethod
    def create_table_row_private_ring(key: PrivateKeyRing):
        return [key.timestamp, key.key_id, key.public_key, key.encrypted_private_key,
                key.user_id]

    def create_table(self):
        table_frame = ttk.Frame(self.dialog_frame)
        table_frame.pack(side=BOTTOM)

        headline_label = ttk.Label(table_frame, text="Select private key to sign the message")
        headline_label.grid(row=0, columnspan=10)

        columns = ['Timestamp', 'Key ID', 'Public Key', 'Encrypted Private Key', 'User ID', 'Select Key']

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
            select_key_button = ttk.Button(actions_frame, text="Select",
                                           command=lambda arg=ring: self.select_ring(arg))
            select_key_button.grid(row=0, column=0)

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)

    def select_ring(self, ring):
        self.parent.private_key_for_sign = ring
        self.send_message_dialog.destroy()
        pass
