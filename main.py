import tkinter as tk

from gui.screens.HomeScreen import HomeScreen


def main():
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
