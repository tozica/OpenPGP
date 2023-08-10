import tkinter as tk
from tkinter import ttk
from gui.tables.PrivateKeyRingTable import PrivateKeyRingTable
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


class PrivateKeyRingDialog:
    def __init__(self, root, parent, email):
        self.root = root
        self.parent = parent
        self.email = email
        self.key_rings = (
            PrivateKeyRing.private_key_ring_by_user)[email] if email in PrivateKeyRing.private_key_ring_by_user else []

        dialog_private_key_table = tk.Toplevel(self.root)
        dialog_private_key_table.title("Private key ring for " + self.email)

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        frame = ttk.Frame(dialog_private_key_table, padding=20)
        frame.pack(fill="both", expand=True)
        PrivateKeyRingTable(self.root, frame, self.parent, self.email, self.key_rings)

        def close():
            dialog_private_key_table.destroy()

        confirm_button = ttk.Button(frame, text="Close", command=close)
        confirm_button.grid(row=5, columnspan=2, pady=10)
