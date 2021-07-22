from tkinter import *
from GUI.MainWindow import *
from time import sleep

class StartWindow():
    pw = "Mein PW"
    password_counter = 0

    def __init__(self):
        self.root = Tk()
        self.root.wm_title("FileLock")
        self.root.geometry("300x60")
        self.root.iconbitmap("Images/applicationicon.ico")
        self.root.eval('tk::PlaceWindow . center')

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
            tkinter.messagebox.showerror("Incorrect password", "You entered the wrong password.\nPlease try again.")
            self.password_counter = self.password_counter + 1
            sleep(self.password_counter)
            self.entry_password.delete(0, 'end')

    def create_widgets(self):
        label_enter_passwordLabel = Label(self.root, text="Enter the password: ")
        label_enter_passwordLabel.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        self.entry_password = Entry(self.root, show="*")
        self.entry_password.grid(column=1, row=0, padx=5, pady=5, sticky=W+E)
        
        button_login = Button(self.root, text="Login")
        button_login.bind('<Button-1>', self.startMainWindow)
        button_login.grid(column=1, row=1, padx=5, pady=5, sticky=W+E)

        self.root.bind('<Return>', self.startMainWindow)