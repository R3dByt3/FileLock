from tkinter import *
from GUI.MainWindow import *

class StartWindow():
    pw = "Mein PW"

    def __init__(self):
        self.root = Tk()
        self.root.wm_title("FileLock")
        self.root.geometry("300x60")
        self.root.iconbitmap("Images/applicationicon.ico")
        self.create_widgets()
    
    def start(self):
        self.root.mainloop()

    def startMainWindow(self):
        if self.entry_password.get() == self.pw:
            self.root.destroy()
            MainWindow().start()
        else:
            self.entry_password.delete(0, 'end')
            tkinter.messagebox.showerror("Incorrect password", "You entered the wrong password.\nPlease try again.")

    def create_widgets(self):
        self.label_enter_passwordLabel = Label(self.root, text="Enter the password: ")
        self.label_enter_passwordLabel.grid(column=0, row=0, padx=5, pady=5)
        self.entry_password = Entry(self.root, show="*", width=15)
        self.entry_password.grid(column=1, row=0, padx=5, pady=5)
        self.button_login = Button(self.root, text="Login", command=self.startMainWindow)
        self.button_login.grid(column=1, row=1)
