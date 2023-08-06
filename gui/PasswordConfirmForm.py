import tkinter as tk
from tkinter import ttk

from des3_utils.des3_utils import perform_decrypt, derive_key_from_password
from gui.TextPreviewPopup import TextPreviewPopup
from key_rings.private_key_utils import compare_passwords


class PasswordConfirmForm:
    def __init__(self, root, parent, value_to_show, ring, headline):
        self.root = root
        self.parent = parent
        self.value_to_show = value_to_show

        new_form = tk.Toplevel(self.root)
        new_form.title("Enter password")

        frame = ttk.Frame(new_form, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Password:").grid(row=0, column=0, sticky="w")
        password_entry = ttk.Entry(frame, show="*")
        password_entry.grid(row=0, column=1)

        def confirm():
            password = password_entry.get()
            if compare_passwords(password, ring):
                decrypted_value = perform_decrypt(ring.d, derive_key_from_password(password, ring.salt))
                TextPreviewPopup(root, decrypted_value, headline, new_form)

        confirm_button = ttk.Button(frame, text="Confirm", command=confirm)
        confirm_button.grid(row=2, columnspan=2, pady=10)
