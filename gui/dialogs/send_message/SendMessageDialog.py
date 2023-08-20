import base64
import json
import tkinter as tk
from ctypes import Union
from tkinter import ttk, TOP, RIGHT, BOTTOM, LEFT
import datetime

from gui.dialogs.general.FolderPicker import FolderPicker
from gui.dialogs.sign_message.SignMessageDialog import SignMessageDialog
from utils.aes_utils import aes_encrypt, aes_decrypt
from utils.des3_utils.des3_utils import perform_encrypt, encrypt_message


class SendMessageDialog:
    def __init__(self, root, parent, email, ring):
        self.root = root
        self.parent = parent
        self.email = email
        self.ring = ring
        self.private_key_for_sign = None
        self.send_message_dialog = tk.Toplevel(self.root)
        self.send_message_dialog.title("Send message")
        self.dialog_frame = ttk.Frame(self.send_message_dialog)
        self.dialog_frame.pack(fill="both", expand=True)
        self.send_path = ""

        self.create_dialog()

    pass

    def create_dialog(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        options_frame = tk.Frame(self.dialog_frame)
        options_frame.pack(side=TOP)
        compress_convert_frame = tk.Frame(options_frame)
        compress_convert_frame.pack(side=RIGHT)
        aes_des_frame = tk.Frame(options_frame)
        aes_des_frame.pack(side=RIGHT)

        sign_message_button = tk.Button(options_frame, text="Sign Message", command=self.sign_message)
        sign_message_button.pack(side=LEFT)
        compress_enabled = tk.IntVar()
        compress_check_box = tk.Checkbutton(compress_convert_frame, text="Compress Message", variable=compress_enabled)
        convert_enabled = tk.IntVar()
        convert_check_box = tk.Checkbutton(compress_convert_frame, text="Convert to radix-64", variable=convert_enabled)
        compress_check_box.pack(side=TOP)
        convert_check_box.pack(side=BOTTOM)
        v = tk.StringVar(value="aes")
        aes_radio_button = tk.Radiobutton(aes_des_frame, text="AES", variable=v, value="aes")
        des_radio_button = tk.Radiobutton(aes_des_frame, text="DES", variable=v, value="des")
        aes_radio_button.pack(side=TOP)
        des_radio_button.pack(side=BOTTOM)

        bottom_frame = tk.Frame(self.dialog_frame)
        bottom_frame.pack(side=BOTTOM)

        text_area_frame = tk.Frame(bottom_frame)
        text_area_frame.pack(side=LEFT)
        text_area_label = tk.Label(text_area_frame, text="Write message below")
        text_area = tk.Text(text_area_frame, height=5, width=30)
        text_area_label.pack(side=TOP)
        text_area.pack(side=BOTTOM)

        def send_message():
            package = {}
            folder_picker = FolderPicker()
            self.send_path = folder_picker.directory + '/' + self.ring.email + '.txt'
            message = text_area.get(1.0, "end-1c")
            timestamp = str(datetime.datetime.now())
            filename = self.send_path
            package["message"] = {
                "data": message,
                "timestamp": timestamp,
                "filename": filename
            }

            # sign message if needed
            if self.private_key_for_sign is not None:
                signature = self.private_key_for_sign.sign_message(message)
                key_id_sender_public_key = self.private_key_for_sign.key_id
                timestamp_signature = str(datetime.datetime.now())
                package["signature"] = {
                    "message_digest": str(signature),
                    "key_id_sender_public_key": key_id_sender_public_key,
                    "timestamp": timestamp_signature
                }

            # encrypt message with selected algorithm
            key_cipher_tuple = ()
            if v.get() == "aes":
                key_cipher_tuple = aes_encrypt(json.dumps(package))

            elif v.get() == "des":
                key_cipher_tuple = encrypt_message(json.dumps(package))

            encrypted_session_key = self.ring.encrypt_session_key(key_cipher_tuple[0])
            key_id_recipient_public_key = self.ring.key_id
            package_to_send = {
                "session_key_component": {
                    "session_key": base64.b64encode(encrypted_session_key).decode('utf-8'),
                    "key_id_of_recipient_public_key": key_id_recipient_public_key,
                    "algorithm": "des" if v.get() == "des" else "aes"
                },
                "encrypted_data": str(key_cipher_tuple[1])
            }

            # compress message if needed
            if compress_enabled.get() == 1:
                # compress message (zip)
                pass

            # convert message if needed
            if convert_enabled.get() == 1:
                # convert message (radix-64)
                pass

            with open(self.send_path, 'w', encoding='utf-8') as send_file:
                json.dump(package_to_send, send_file, ensure_ascii=False, indent=4)

        pass

        commands_frame = tk.Frame(bottom_frame)
        commands_frame.pack(side=RIGHT)
        send_message_button = tk.Button(bottom_frame, text="Send message", command=send_message)
        send_message_button.pack(side=BOTTOM)

    def sign_message(self):
        SignMessageDialog(self.root, self, self.email, self.ring)
        pass
