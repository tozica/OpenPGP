import tkinter as tk
from tkinter import ttk, TOP, RIGHT, BOTTOM, LEFT


class SendMessageDialog:
    def __init__(self, root, parent, email, ring):
        self.root = root
        self.parent = parent
        self.email = email
        self.ring = ring
        self.send_message_dialog = tk.Toplevel(self.root)
        self.send_message_dialog.title("Send message")
        self.dialog_frame = ttk.Frame(self.send_message_dialog)
        self.dialog_frame.pack(fill="both", expand=True)

        self.create_dialog()
    pass

    def create_dialog(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        options_frame = tk.Frame(self.dialog_frame)
        options_frame.pack(side=TOP)

        sign_message_button = tk.Button(options_frame, text="Sign Message")
        sign_message_button.pack(side=LEFT)
        compress_enabled = tk.IntVar()
        compress_check_box = tk.Checkbutton(options_frame, text="Compress Message", variable=compress_enabled)
        convert_enabled = tk.IntVar()
        convert_check_box = tk.Checkbutton(options_frame, text="Convert to radix-64", variable=convert_enabled)
        compress_check_box.pack(side=RIGHT)
        convert_check_box.pack(side=RIGHT)

        bottom_frame = tk.Frame(self.dialog_frame)
        bottom_frame.pack(side=BOTTOM)

        text_area_frame = tk.Frame(bottom_frame)
        text_area_frame.pack(side=LEFT)
        text_area_label = tk.Label(text_area_frame, text="Write message below")
        text_area = tk.Text(text_area_frame, height=5, width=30)
        text_area_label.pack(side=TOP)
        text_area.pack(side=BOTTOM)

        commands_frame = tk.Frame(bottom_frame)
        commands_frame.pack(side=RIGHT)
        send_message_button = tk.Button(bottom_frame, text="Send message")
        send_message_button.pack(side=BOTTOM)
        pass
