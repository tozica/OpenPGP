from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class FilePicker:
    def __init__(self):
        filetypes = (
            ('Pem files', '*.pem'),
            ('Text files', '*.txt'),
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