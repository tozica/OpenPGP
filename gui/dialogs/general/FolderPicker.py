from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class FolderPicker:
    def __init__(self):

        self.directory = fd.askdirectory(
            title='Open folder',
            initialdir='/')

        showinfo(
            title='Selected Folder',
            message=self.directory
        )
