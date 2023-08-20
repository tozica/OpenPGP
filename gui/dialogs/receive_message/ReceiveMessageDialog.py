import tkinter as tk
from tkinter import ttk, TOP, BOTTOM, scrolledtext


class ReceiveMessageDialog:
    def __init__(self, root, parent, message, sender_email, receiver_email):
        self.root = root
        self.parent = parent
        self.receive_message_dialog = tk.Toplevel(self.root)
        self.receive_message_dialog.title("Received message")
        self.dialog_frame = ttk.Frame(self.receive_message_dialog)
        self.dialog_frame.pack(fill="both", expand=True)

        self.timestamp = message["timestamp"]
        self.data = message["data"]
        self.file_name = message["filename"]
        self.sender_email = sender_email
        self.receiver_email = receiver_email

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

        data_frame = ttk.Frame(self.dialog_frame)
        data_frame.pack(side=BOTTOM)
        ttk.Label(data_frame, text="Your message is below: ").pack(side=TOP)
        text_widget = scrolledtext.ScrolledText(data_frame, wrap=tk.WORD, width=40, height=10)
        text_widget.insert(tk.END, self.data)
        text_widget.pack(side=BOTTOM)
