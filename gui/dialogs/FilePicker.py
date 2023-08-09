from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class FilePicker:
    def __init__(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        self.directory = fd.askdirectory(
            title='Open folder',
            initialdir='/')

        showinfo(
            title='Selected Folder',
            message=self.directory
        )
