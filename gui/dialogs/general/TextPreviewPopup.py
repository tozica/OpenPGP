import tkinter as tk
from tkinter import scrolledtext


class TextPreviewPopup:
    def __init__(self, root, text, headline, parent=None):
        popup = tk.Toplevel(root)
        popup.title(headline)

        text_widget = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=40, height=10)
        text_widget.insert(tk.END, text)
        text_widget.pack(fill=tk.BOTH, expand=True)

        def close_popup():
            popup.destroy()
            if parent is not None:
                parent.destroy()

        close_button = tk.Button(popup, text="Close", command=close_popup)
        close_button.pack()
