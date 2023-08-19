from tkinter import ttk, LEFT
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


class UserDetailsTable:
    def __init__(self, root, frame, parent, email):
        self.frame = frame
        self.root = root
        self.parent = parent
        self.button_data = [
            ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "1,7"],
            ["2,1", "2,2", "2,3", "2,4", "2,5", "2,6", "2,7"],
            ["3,1", "3,2", "3,3", "3,4", "3,5", "3,6", "3,7"],
        ]
        self.email = email
        self.create_table()

    @property
    def user_information(self):
        key = PrivateKeyRing.private_key_ring_by_user[self.email][0] if self.email in PrivateKeyRing.private_key_ring_by_user else None
        return [key.user_id, key.user_name, key.email, str(len(PrivateKeyRing.private_key_ring_by_user[self.email]))] if key is not None else []

    def create_table(self):
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(side=LEFT)

        headline_label = ttk.Label(table_frame, text="User Information")
        headline_label.grid(row=0, columnspan=4)

        columns = ['User Id', 'User Name', 'Email', 'Number of keys pairs']

        for col_idx, col_name in enumerate(columns):
            col_label = ttk.Label(table_frame, text=col_name, borderwidth=1, relief="solid", padding=5)
            col_label.grid(row=1, column=col_idx, sticky="nsew")

            self.root.grid_columnconfigure(col_idx, weight=1)

        for col_idx, cell_value in enumerate(self.user_information):
            cell_label = ttk.Label(table_frame, text=str(cell_value)[:20], borderwidth=1, relief="solid", padding=5)
            cell_label.grid(row=2, column=col_idx, sticky="nsew")

        for row_idx in range(len(self.button_data) + 2):
            table_frame.grid_rowconfigure(row_idx, weight=1)
