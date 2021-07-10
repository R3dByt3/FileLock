from tkinter import *
from tkinter import filedialog


class GUI(Frame):
    def __init__(self, window):
        Frame.__init__(self)
        label = Label(self, text="Hallo")

        label_file_explorer = Label(window,
                                    text="File Explorer using Tkinter",
                                    width=100, height=4, fg="blue")

        button_explore = Button(window,
                                text="Browse Files",
                                command=fileBrowser)

        button_exit = Button(window,
                             text="Exit",
                             command=exit)

        label_file_explorer.grid(column=1, row=1)

        button_explore.grid(column=1, row=2)

        button_exit.grid(column=1, row=3)

        label.pack()


"""
    def fileBrowser():
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select file",
                                              filetypes=(("all files", "*")))

        label_file_explorer.configure(text="File Opened: "+filename)
        """
