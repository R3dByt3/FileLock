from tkinter import *
from os import *
from GUI.MainWindow import *
from time import sleep
from Encryption.crypto import encrypter

class StartWindow():
    __password_counter = 0
    __dbPath = join(dirname(dirname(realpath(__file__))), "db.db")

    def __init__(self):
        self.root = Tk()
        self.root.wm_title("FileLock")
        self.set_geometry_start_window()
        icon_path = join(dirname(dirname(realpath(__file__))), "Images", "applicationicon.ico")
        self.root.iconbitmap(icon_path)

        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=2)

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=1)

        self.create_widgets()

    def start(self):
        self.root.mainloop()

    def set_geometry_start_window(self):
        application_width = 300
        frame_width = self.root.winfo_rootx() - self.root.winfo_x()
        window_width = application_width + 2 * frame_width

        application_height = 60
        titlebar_height = self.root.winfo_rooty() - self.root.winfo_y()
        window_height = application_height + titlebar_height + frame_width

        x = self.root.winfo_screenwidth() // 2 - window_width // 2
        y = self.root.winfo_screenheight() // 2 - window_height // 2
        self.root.geometry('{}x{}+{}+{}'.format(application_width, application_height, x, y))

    def start_main_window(self, event):
        if path.exists(self.__dbPath):
            try:
                crypter = encrypter(self.__dbPath, self.entry_password.get())
            except Exception:
                tkinter.messagebox.showerror("Incorrect password", "You entered the wrong password.\nPlease try again.")
                self.__password_counter = self.__password_counter + 1
                sleep(self.__password_counter)
                self.entry_password.delete(0, 'end')
                return
        else:
            tkinter.messagebox.showinfo("New database created", "You created a new database with the entered password.")
            crypter = encrypter(self.__dbPath, self.entry_password.get())

        self.root.destroy()
        MainWindow(crypter).start()

    def create_widgets(self):
        label_enter_password = Label(self.root, text="Enter the password: ")
        label_enter_password.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        self.entry_password = Entry(self.root, show="*")
        self.entry_password.grid(column=1, row=0, padx=5, pady=5, sticky=W+E)
        
        button_login = Button(self.root, text="Login")
        button_login.bind('<Button-1>', self.start_main_window)
        button_login.grid(column=1, row=1, padx=5, pady=5, sticky=W+E)

        self.root.bind('<Return>', self.start_main_window)