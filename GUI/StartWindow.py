from tkinter import *
from GUI.MainWindow import *

class StartWindow():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Enter password")
        self.root.iconbitmap("Images/applicationicon.ico")
        self.create_widgets()
    
    def start(self):
        self.root.mainloop()

    def startMainWindow(self):
        self.root.destroy()
        MainWindow().start()

    def create_widgets(self):
        self.label_enter_passwordLabel = Label(self.root, text="Select the files you want to encrypt: ")
        self.label_enter_passwordLabel.grid(column=0, row=0)
        self.entry_password = Entry(self.root, show="*", width=15)
        self.entry_password.grid(column=1, row=0)
        self.button_login = Button(self.root, text="Login", command=self.startMainWindow)
        self.button_login.grid(column=1, row=1)
