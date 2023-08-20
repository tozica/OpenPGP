from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class FilePicker:
    def __init__(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=self.filename
        )