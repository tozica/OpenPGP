import tkinter as tk

from gui.screens.HomeScreen import HomeScreen
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


def main():
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
