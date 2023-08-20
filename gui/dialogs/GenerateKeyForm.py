import tkinter as tk
from datetime import date
from tkinter import ttk

from key_rings.base_key_ring.private_key_ring import PrivateKeyRing
from key_rings.elgamal_key_ring.elgamal_private_key_ring import ElgamalPrivateKeyRing
from key_rings.rsa_key_ring.rsa_private_key_ring import RSAPrivateKeyRing
from utils.des3_utils.des3_utils import perform_encrypt
from utils.rsa_util import rsa_util
from elgamal.elgamal import Elgamal


class GenerateKeyForm:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

        new_form = tk.Toplevel(self.root)
        new_form.title("Generate keys")

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        frame = ttk.Frame(new_form, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w")
        ttk.Label(frame, text="Key Size:").grid(row=2, column=0, sticky="w")
        ttk.Label(frame, text="Algorithm:").grid(row=3, column=0, sticky="w")
        ttk.Label(frame, text="Password:").grid(row=4, column=0, sticky="w")

        name_entry = ttk.Entry(frame)
        email_entry = ttk.Entry(frame)
        key_size_entry = ttk.Entry(frame)
        password_entry = ttk.Entry(frame, show="*")

        name_entry.grid(row=0, column=1)
        email_entry.grid(row=1, column=1)
        key_size_entry.grid(row=2, column=1)

        algorithm_var = tk.StringVar()
        ttk.Label(frame, text="Algorithm:").grid(row=3, column=0, sticky="w")

        algorithms = ["Elgamal & DSA", "RSA"]
        for index, algorithm in enumerate(algorithms):
            ttk.Radiobutton(frame, text=algorithm, variable=algorithm_var, value=algorithm).grid(row=3,
                                                                                                 column=index + 1,
                                                                                                 sticky="w")

        password_entry.grid(row=4, column=1)

        def confirm():
            name = name_entry.get()
            email = email_entry.get()
            key_size = key_size_entry.get()
            selected_algorithm = algorithm_var.get()
            password = password_entry.get()

            if selected_algorithm == "RSA":
                (public_rsa, private_rsa) = rsa_util.generate_keys(int(key_size))

                key_from_password, encrypted_private_key, salt = perform_encrypt(private_rsa.d, password)

                rsa_key_ring = RSAPrivateKeyRing(date.today(), email, email, "RSA",
                                                 int(key_size), name, encrypted_private_key, key_from_password,
                                                 private_rsa, public_rsa)

                PrivateKeyRing.insert_row(email, rsa_key_ring)

            elif selected_algorithm == "Elgamal & DSA":
                (public_elgamal, private_elgamal) = Elgamal.newkeys(int(key_size))

                key_from_password, encrypted_private_key, salt = perform_encrypt(private_elgamal.x, password)

                elgamal_key_ring = ElgamalPrivateKeyRing(date.today(), email, email, "Elgamal & DSA", int(key_size),
                                                         name, encrypted_private_key, key_from_password,
                                                         private_elgamal, public_elgamal)

                PrivateKeyRing.insert_row(email, elgamal_key_ring)

            new_form.destroy()
            parent.render()

        confirm_button = ttk.Button(frame, text="Confirm", command=confirm)
        confirm_button.grid(row=5, columnspan=2, pady=10)
