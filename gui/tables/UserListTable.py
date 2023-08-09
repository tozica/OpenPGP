from tkinter import ttk
from gui.dialogs.PrivateKeyRingDialog import PrivateKeyRingDialog
from gui.dialogs.PublicKeyRingDialog import PublicKeyRingDialog
from key_rings.key_ring import KeyRing


class UserListTable:
    def __init__(self, root, frame, parent):
        self.frame = frame
        self.root = root
        self.parent = parent
        self.button_data = [
            ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "1,7"],
            ["2,1", "2,2", "2,3", "2,4", "2,5", "2,6", "2,7"],
            ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7"],
        ]
        self.create_table()

    @staticmethod
    def user_information(key_ring):
        key = key_ring[0]
        return [key.user_id, key.user_name, key.email]

    def create_table(self):
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=1, column=0)

        headline_label = ttk.Label(table_frame, text="Registered User List")
        headline_label.grid(row=0, columnspan=4)

        columns = ['User Id', 'User Name', 'Email', 'Actions']

        for col_idx, col_name in enumerate(columns):
            col_label = ttk.Label(table_frame, text=col_name, borderwidth=1, relief="solid", padding=5)
            col_label.grid(row=1, column=col_idx, sticky="nsew")

            self.root.grid_columnconfigure(col_idx, weight=1)

        for row_idx, (user_email, key_rings) in enumerate(KeyRing.key_rings_by_user.items()):
            for col_idx, cell_value in enumerate(self.user_information(key_rings)):
                cell_label = ttk.Label(table_frame, text=str(cell_value)[:20], borderwidth=1, relief="solid", padding=5)
                cell_label.grid(row=row_idx + 2, column=col_idx, sticky="nsew")

            actions_frame = ttk.Frame(table_frame)
            actions_frame.grid(row=row_idx + 2, column=3, sticky="nsew")
            show_private_ring_button = ttk.Button(actions_frame, text="Private Ring",
                                                  command=lambda email=user_email, key_ring=key_rings:
                                                  PrivateKeyRingDialog(self.root, self, email, key_ring))
            show_public_ring_button = ttk.Button(actions_frame, text="Public Ring",
                                                 command=lambda email=user_email, key_ring=key_rings:
                                                 PublicKeyRingDialog(self.root, self, email, key_ring))
            delete_user_button = ttk.Button(actions_frame, text="Delete User",
                                            command=lambda email=user_email: self.delete_user(email))

            show_private_ring_button.grid(row=0, column=0)
            show_public_ring_button.grid(row=0, column=1)
            delete_user_button.grid(row=0, column=2)

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)

    def delete_user(self, email):
        del KeyRing.key_rings_by_user[email]
        self.parent.render()
