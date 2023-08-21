import tkinter as tk
from tkinter import ttk, TOP, BOTTOM, scrolledtext

from key_rings.base_key_ring.public_key_ring import PublicKeyRing


class ReceiveMessageDialog:
    def __init__(self, root, parent, message_and_signature, receiver_email):
        self.root = root
        self.parent = parent
        self.receive_message_dialog = tk.Toplevel(self.root)
        self.receive_message_dialog.title("Received message")
        self.dialog_frame = ttk.Frame(self.receive_message_dialog)
        self.dialog_frame.pack(fill="both", expand=True)

        self.timestamp = message_and_signature["message"]["timestamp"]
        self.data = message_and_signature["message"]["data"]
        self.file_name = message_and_signature["message"]["filename"]
        test = message_and_signature["signature"]["key_id_sender_public_key"]
        public_sender_key = PublicKeyRing.find_key_by_id(message_and_signature["signature"]["key_id_sender_public_key"])
        self.sender_email = public_sender_key.email if public_sender_key is not None else None
        self.receiver_email = receiver_email

        self.create_dialog()

    def create_dialog(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        information_frame = ttk.Frame(self.dialog_frame)
        information_frame.pack(side=TOP)

        ttk.Label(information_frame, text="Timestamp: " + self.timestamp).grid(row=0, column=0, sticky="w")
        ttk.Label(information_frame, text="Sender's email: " + self.sender_email).grid(row=1, column=0, sticky="w")
        ttk.Label(information_frame, text="Receiver's email: " + self.receiver_email).grid(row=2, column=0, sticky="w")
        ttk.Label(information_frame, text="Received from inbox: " + self.file_name).grid(row=3, column=0, sticky="w")
        ttk.Label(information_frame, text="Message is signed: " + "YES" if self.sender_email is not None else "NO").grid(row=3, column=0, sticky="w")

        data_frame = ttk.Frame(self.dialog_frame)
        data_frame.pack(side=BOTTOM)
        ttk.Label(data_frame, text="Your message is below: ").pack(side=TOP)
        text_widget = scrolledtext.ScrolledText(data_frame, wrap=tk.WORD, width=40, height=10)
        text_widget.insert(tk.END, self.data)
        text_widget.pack(side=BOTTOM)
