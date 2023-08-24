import json
import re
import tkinter as tk
from tkinter import ttk, TOP, RIGHT

from gui.dialogs.general.FilePicker import FilePicker
from gui.tables.key_rings.PublicKeyRingTable import PublicKeyRingTable
from gui.tables.user.UserDetailsTable import UserDetailsTable
from key_rings.base_key_ring.public_key_ring import PublicKeyRing
from key_rings.elgamal_key_ring.elgamal_public_key_ring import ElgamalPublicKeyRing
from key_rings.rsa_key_ring.rsa_public_key_ring import RSAPublicKeyRing


class PublicKeyRingDialog:
    def __init__(self, root, parent, email):
        self.root = root
        self.parent = parent
        self.email = email
        self.key_rings = PublicKeyRing.public_key_ring_by_user[
            email] if email in PublicKeyRing.public_key_ring_by_user else []
        self.dialog_private_key_table = tk.Toplevel(self.root)
        self.dialog_private_key_table.title("Public key ring for " + self.email)
        self.dialog_frame = ttk.Frame(self.dialog_private_key_table)
        self.dialog_frame.pack(fill="both", expand=True)

        self.create_dialog()

    def clear_window(self):
        for widget in self.dialog_frame.winfo_children():
            widget.destroy()

    def create_dialog(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        user_information_fame = ttk.Frame(self.dialog_frame)
        user_information_fame.pack(side=TOP)
        UserDetailsTable(self.root, user_information_fame, self, self.email)

        import_key_button = ttk.Button(user_information_fame, text="Import Key",
                                       command=lambda arg=self.email: self.import_public_ring(arg))
        import_key_button.pack(side=RIGHT)

        PublicKeyRingTable(self.root, self.dialog_frame, self, self.email, self.key_rings)

        confirm_button = ttk.Button(user_information_fame, text="Close",
                                    command=lambda: self.dialog_private_key_table.destroy())
        confirm_button.pack(side=RIGHT)
        pass

    def render(self):
        self.clear_window()
        self.create_dialog()
        pass

    def import_public_ring(self, email):
        file_picker = FilePicker()

        if file_picker.filename == '':
            return

        metadata = self.get_methadata(file_picker.filename)

        if metadata["algorithm"] == "RSA":
            RSAPublicKeyRing.import_public_key(file_picker.filename, metadata, email)
        elif metadata["algorithm"] == "Elgamal & DSA":
            ElgamalPublicKeyRing.import_public_key(file_picker.filename, metadata, email)

        self.render()

    def get_methadata(self, path):
        file_name = path.split("/")[len(path.split("/")) - 1]
        metadata_file_path = re.sub(file_name, ".metadata", path)
        with open(metadata_file_path, mode='r') as metadata_file:
            metadata = json.load(metadata_file)

        return metadata
