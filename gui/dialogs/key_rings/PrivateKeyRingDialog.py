import base64
import io
import json
import re
import tkinter as tk
import zipfile
from tkinter import ttk
from tkinter.constants import TOP, RIGHT

from gui.dialogs.general.FilePicker import FilePicker
from gui.dialogs.general.FolderPicker import FolderPicker
from gui.dialogs.receive_message.ReceiveMessageDialog import ReceiveMessageDialog
from gui.tables.key_rings.PrivateKeyRingTable import PrivateKeyRingTable
from gui.tables.user.UserDetailsTable import UserDetailsTable
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing
from key_rings.base_key_ring.public_key_ring import PublicKeyRing
from key_rings.elgamal_key_ring.elgamal_private_key_ring import ElgamalPrivateKeyRing
from key_rings.rsa_key_ring.rsa_private_key_ring import RSAPrivateKeyRing
from utils.aes_utils.aes_utils import aes_decrypt
from utils.des3_utils.des3_utils import decrypt_message


class PrivateKeyRingDialog:
    def __init__(self, root, parent, email):
        self.root = root
        self.parent = parent
        self.email = email
        self.key_rings = (
            PrivateKeyRing.private_key_ring_by_user)[email] if email in PrivateKeyRing.private_key_ring_by_user else []
        self.dialog_private_key_table = tk.Toplevel(self.root)
        self.dialog_private_key_table.title("Private key ring for " + self.email)
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

        receive_button = ttk.Button(user_information_fame, text="Receive message",
                                    command=lambda: self.receive_message())
        receive_button.pack(side=RIGHT)

        import_private_key_button = ttk.Button(user_information_fame, text="Import Private Key",
                                               command=self.import_private_ring)
        import_private_key_button.pack(side=RIGHT)

        PrivateKeyRingTable(self.root, self.dialog_frame, self, self.email, self.key_rings)

        confirm_button = ttk.Button(user_information_fame, text="Close",
                                    command=lambda: self.dialog_private_key_table.destroy())
        confirm_button.pack(side=RIGHT)

    @staticmethod
    def import_private_ring():
        file_picker = FilePicker()
        if file_picker.filename != '':
            path = file_picker.filename
            pem_file_path = path
            file_name = path.split("/")[len(path.split("/")) - 1]
            metadata_file_path = re.sub(file_name, ".metadata", path)

            with open(metadata_file_path, mode='r') as metadata_file:
                metadata = json.load(metadata_file)

            if metadata["algorithm"] == "RSA":
                RSAPrivateKeyRing.import_private_key(pem_file_path)
            else:
                ElgamalPrivateKeyRing.import_private_key(pem_file_path)

    def render(self):
        self.clear_window()
        self.create_dialog()
        pass

    def receive_message(self):
        package = {}
        file_picker = FilePicker()
        received_file_path = file_picker.filename

        with open(received_file_path, mode='r') as received_file:
            unpacked_package = json.load(received_file)

        encrypted_session_key = base64.b64decode(unpacked_package["session_key_component"]["session_key"])
        key_id_of_recipient_public_key = unpacked_package["session_key_component"]["key_id_of_recipient_public_key"]
        algorithm = unpacked_package["session_key_component"]["algorithm"]
        encrypted_data = base64.b64decode(unpacked_package["encrypted_data"])
        compress = unpacked_package["session_key_component"]["compress"]

        private_key_ring = PrivateKeyRing.find_key_by_id(key_id_of_recipient_public_key)
        session_key = private_key_ring.decrypt_session_key(encrypted_session_key)

        decrypted_message = None
        if algorithm == "des":
            decrypted_message = decrypt_message(encrypted_data, session_key)
        elif algorithm == "aes":
            decrypted_message = aes_decrypt(bytes(session_key), encrypted_data)

        if compress == 1:
            try:
                byte_stream = io.BytesIO(decrypted_message)
                zip_file = zipfile.ZipFile(byte_stream, 'r')

                file_contents = zip_file.read('data.txt')
                decrypted_message = file_contents.decode('utf-8')

            except Exception as ex:
                aaa = "a"
                pass

        message_and_signature = json.loads(decrypted_message)

        # verify signature if needed
        if message_and_signature.get("signature", None) is not None:
            public_sender_key = PublicKeyRing.find_key_by_id(
                message_and_signature["signature"]["key_id_sender_public_key"])
            public_sender_key.verify_sign(base64.b64encode(message_and_signature["message"]["data"].encode()),
                                          base64.b64decode(message_and_signature["signature"]["message_digest"]))
            pass

        # show message
        print(message_and_signature["message"]["data"])

        ReceiveMessageDialog(self.root, self, message_and_signature, self.email)
        pass
