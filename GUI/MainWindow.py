from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from GUI.ContextMenuListBox import ContextMenuListBox

class MainWindow():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("File encryptor")
        self.root.iconbitmap("Images/applicationicon.ico")
        self.create_widgets()

    def start(self):
        self.root.mainloop()

    def buttonEncryptionClick(self):
        dosomething = True
        if dosomething == True:
            tkinter.messagebox.showinfo("Encryption succeeded", "All file were encrypted.")
        else:
            tkinter.messagebox.showerror("Encryption failed", "Encryption failed")

    def buttonDecryptionClick(self):
        dosomething = False
        if dosomething:
            tkinter.messagebox.showinfo("Decryption succeeded", "All file were decrypted.")
        else:
            tkinter.messagebox.showerror("Decryption failed", "Decryption failed")

    def openFileDialog(self):
        filenames = askopenfilenames()
        for element in filenames:
            self.listbox_encrypt_files.insert("end", element)
        self.label_encrypted_files_counter_text.set("{} of {} files were encrypted".format(self.listbox_encrypt_files.size(), self.listbox_encrypt_files.size()))

    def create_widgets(self):
        self.label_select_files = Label(self.root, text="Select the files you want to encrypt: ")
        self.label_select_files.grid(column=0, row=0, padx='5', pady='5', sticky='ew')

        self.button_open_file_explorer = Button(self.root, text="Open file explorer", command=self.openFileDialog)
        self.button_open_file_explorer.grid(column=1, row=0, padx='5', pady='5', sticky='ew')

        self.listbox_encrypt_files = ContextMenuListBox(self.root, selectmode='multiple')
        self.listbox_encrypt_files.grid(column=0, columnspan=2, row=1, padx='5', pady='5', sticky='ew')

        self.listbox_decrypt_files = Listbox(self.root, selectmode='multiple')
        self.listbox_decrypt_files.grid(column=2, columnspan=2, row=1, padx='5', pady='5', sticky='ew')

        self.label_encrypted_files_counter_text = StringVar()
        self.label_encrypted_files_counter_text.set("{} of {} files were encrypted".format(self.listbox_encrypt_files.size(), self.listbox_encrypt_files.size()))
        self.label_encrypted_files_counter = Label(self.root, textvariable=self.label_encrypted_files_counter_text)
        self.label_encrypted_files_counter.grid(column=0, columnspan=2, row=2)

        self.button_encrypt_files = Button(self.root, text="Encrypt", command=self.buttonEncryptionClick)
        self.button_encrypt_files.grid(column=0, columnspan=2, row=3, padx='5', pady='5', sticky='ew')

        self.button_decrypt_files = Button(self.root, text="Decrypt", command=self.buttonDecryptionClick)
        self.button_decrypt_files.grid(column=2, columnspan=2, row=3, padx='5', pady='5', sticky='ew')

        self.button_exit = Button(self.root, text="Exit", command=exit)
        self.button_exit.grid(column=1, row=3, padx='5', pady='5', sticky='ew')