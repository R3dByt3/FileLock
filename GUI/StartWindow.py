from os.path import *
from tkinter import *
from GUI.MainWindow import *


class StartWindow():
    pw = "Mein PW"

    def __init__(self):
        path = join(dirname(dirname(realpath(__file__))),
                    "Images", "applicationicon.ico")
        self.root = Tk()
        self.root.wm_title("FileLock")
        self.root.geometry("300x60")
        self.root.iconbitmap(path)
        self.root.eval('tk::PlaceWindow . center')

        self.password_frame = Frame(self.root)

        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=2)

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=1)

        self.create_widgets()

    def start(self):
        self.root.mainloop()

    def startMainWindow(self, event):
        if self.entry_password.get() == self.pw:
            self.root.destroy()
            MainWindow().start()
        else:
            self.entry_password.delete(0, 'end')
            tkinter.messagebox.showerror(
                "Incorrect password", "You entered the wrong password.\nPlease try again.")

    def create_widgets(self):
        label_enter_passwordLabel = Label(
            self.root, text="Enter the password: ")
        label_enter_passwordLabel.grid(
            column=0, row=0, padx=5, pady=5, sticky=W)
        self.entry_password = Entry(self.root, show="*")
        self.entry_password.grid(column=1, row=0, padx=5, pady=5, sticky=W+E)
        button_login = Button(self.root, text="Login")
        button_login.bind('<Button-1>', self.startMainWindow)
        button_login.grid(column=1, row=1, padx=5, pady=5, sticky=W+E)
        self.root.bind('<Return>', self.startMainWindow)
