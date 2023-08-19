import tkinter as tk
from tkinter import ttk, TOP, RIGHT, BOTTOM

from gui.dialogs.general.FilePicker import FilePicker
from gui.tables.key_rings.PublicKeyRingTable import PublicKeyRingTable
from gui.tables.user.UserDetailsTable import UserDetailsTable
from key_rings.base_key_ring.public_key_ring import PublicKeyRing
from key_rings.rsa_key_ring.rsa_public_key_ring import RSAPublicKeyRing


class PublicKeyRingDialog:
    def __init__(self, root, parent, email):
        self.root = root
        self.parent = parent
        self.email = email
        self.key_rings = PublicKeyRing.public_key_ring_by_user[email] if email in PublicKeyRing.public_key_ring_by_user else []

        dialog_private_key_table = tk.Toplevel(self.root)
        dialog_private_key_table.title("Public key ring for " + self.email)

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        dialog_frame = ttk.Frame(dialog_private_key_table)
        dialog_frame.pack(fill="both", expand=True)

        user_information_fame = ttk.Frame(dialog_frame)
        user_information_fame.pack(side=TOP)
        UserDetailsTable(self.root, user_information_fame, self, self.email)

        import_key_button = ttk.Button(user_information_fame, text="Import Key",
                                       command=lambda arg=email: self.import_public_ring(arg))
        import_key_button.pack(side=RIGHT)

        PublicKeyRingTable(self.root, dialog_frame, self.parent, self.email, self.key_rings)

        def close():
            dialog_private_key_table.destroy()

        confirm_button = ttk.Button(user_information_fame, text="Close", command=close)
        confirm_button.pack(side=RIGHT)

    @staticmethod
    def import_public_ring(email):
        file_picker = FilePicker()
        RSAPublicKeyRing.import_public_key(file_picker.filename, email)
    pass
