from Encryption.crypto import encrypter
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilenames
from GUI.ContextMenuListBox import ContextMenuListBox
from tkinter import ttk
from os.path import *

class MainWindow():
    crypter: encrypter = None

    def __init__(self, crypter: encrypter):
        path = join(dirname(dirname(realpath(__file__))),
                    "Images", "applicationicon.ico")
        
        self.crypter = crypter

        self.root = Tk()
        self.root.wm_title("File encryptor")
        self.root.iconbitmap(path)
        self.root.geometry("500x500")
        self.root.eval('tk::PlaceWindow . center')

        self.tab_control = ttk.Notebook(self.root)

        self.encrypt_tab = Frame(self.tab_control)
        self.decrypt_tab = Frame(self.tab_control)

        self.init_encrypt_tab()
        self.init_decrypt_tab()

        self.tab_control.add(self.encrypt_tab, text='Encrypt')
        self.tab_control.add(self.decrypt_tab, text='Decrypt')

        self.tab_control.pack(expand=1, fill="both")

    def start(self):
        self.root.mainloop()

    def getEncryptedFiles(self):
        files = self.crypter.read_files()
        for element in files:
            self.listbox_decrypt_files.insert("end", element)

    def openFileDialog(self):
        filenames = askopenfilenames()
        for element in filenames:
            self.listbox_encrypt_files.insert("end", element)

    def buttonEncryptionClick(self):
        selectedItems = self.listbox_encrypt_files.curselection()

        if selectedItems == ((),):
            tkinter.messagebox.showerror(
                "Encryption failed", "No files selected")
            return

        counter = 0
        simpleMode = True

        if self.encryption_type_combobox.current() == 1:
            simpleMode = False

        for selectedItem in selectedItems:
            bytearrayFile = open(
                self.listbox_encrypt_files.get(selectedItem), "rb").read()

            if simpleMode:
                wasSuccessful = self.crypter.encrypt(bytearrayFile)
            else:
                wasSuccessful = self.crypter.encrypt2(bytearrayFile)

            if not wasSuccessful:
                tkinter.messagebox.showerror(
                    "Encryption failed", "Encryption failed")
                return

            counter = counter + 1
            self.label_encrypted_files_counter_text.set(
                "{} of {} files were encrypted".format(counter, len(selectedItems)))
            self.listbox_encrypt_files.update()

        tkinter.messagebox.showinfo(
            "Encryption succeeded", "All files were encrypted.")
        
        self.getEncryptedFiles()

    def buttonDecryptionClick(self):
        selectedItems = self.listbox_decrypt_files.curselection()

        if selectedItems == ((),):
            tkinter.messagebox.showerror(
            "Encryption failed", "No files selected")
            return

        counter = 0

        for selectedItem in selectedItems:
            wasSuccessful = self.crypter.decrypt(selectedItem)

            if not wasSuccessful:
                tkinter.messagebox.showerror(
                    "Decryption failed", "Decryption failed")
                return

            counter = counter + 1
            self.label_decrypted_files_counter_text.set(
                "{} of {} files were decrypted".format(counter, len(selectedItems)))
            self.listbox_decrypt_files.update()

    def init_encrypt_tab(self):
        Grid.columnconfigure(self.encrypt_tab, 0, weight=1)
        Grid.columnconfigure(self.encrypt_tab, 1, weight=1)

        Grid.rowconfigure(self.encrypt_tab, 0, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 1, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 2, weight=1)
        Grid.rowconfigure(self.encrypt_tab, 3, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 4, weight=0)

        label_select_files = Label(
            self.encrypt_tab, text="Select the files you want to encrypt: ")
        label_select_files.grid(column=0, row=0, padx='5', pady='5', sticky=W)

        button_open_file_explorer = Button(
            self.encrypt_tab, text="Open file explorer", command=self.openFileDialog)
        button_open_file_explorer.grid(
            column=1, row=0, padx='5', pady='5', sticky=E+W)

        self.encryption_type_combobox = ttk.Combobox(self.encrypt_tab, state="readonly", values=[
                                                     "Simple", "Extended (Needs more storage)"])
        self.encryption_type_combobox.grid(
            column=0, columnspan=2, row=1, padx=5, pady=5, sticky=E+W)
        self.encryption_type_combobox.current(0)

        self.listbox_encrypt_files = ContextMenuListBox(
            self.encrypt_tab, selectmode='multiple')
        self.listbox_encrypt_files.grid(
            column=0, columnspan=2, row=2, padx='5', pady='5', sticky=N+E+S+W)
        self.listbox_encrypt_files.configure(selectbackground="dimgray")

        scrollbar = Scrollbar(self.listbox_encrypt_files, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_encrypt_files.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_encrypt_files.yview)

        self.label_encrypted_files_counter_text = StringVar()
        self.label_encrypted_files_counter_text.set("")
        self.label_encrypted_files_counter = Label(
            self.encrypt_tab, textvariable=self.label_encrypted_files_counter_text)
        self.label_encrypted_files_counter.grid(
            column=0, columnspan=2, row=3, sticky=E+W)

        button_encrypt_files = Button(
            self.encrypt_tab, text="Encrypt", command=self.buttonEncryptionClick)
        button_encrypt_files.grid(
            column=0, columnspan=2, row=4, padx='5', pady='5', sticky=E+W)

    def init_decrypt_tab(self):
        Grid.columnconfigure(self.decrypt_tab, 0, weight=1)

        Grid.rowconfigure(self.decrypt_tab, 0, weight=0)
        Grid.rowconfigure(self.decrypt_tab, 1, weight=1)
        Grid.rowconfigure(self.decrypt_tab, 2, weight=0)
        Grid.rowconfigure(self.decrypt_tab, 3, weight=0)

        label_select_files_decrypt = Label(
            self.decrypt_tab, text="Select the files you want to decrypt: ")
        label_select_files_decrypt.grid(
            column=0, row=0, padx='5', pady='5', sticky=W)

        self.listbox_decrypt_files = Listbox(
            self.decrypt_tab, selectmode='multiple')
        self.listbox_decrypt_files.grid(
            column=0, row=1, padx='5', pady='5', sticky=N+E+S+W)
        self.listbox_decrypt_files.configure(selectbackground="dimgray")

        self.getEncryptedFiles()

        scrollbar = Scrollbar(self.listbox_decrypt_files, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_decrypt_files.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_decrypt_files.yview)

        self.label_decrypted_files_counter_text = StringVar()
        self.label_decrypted_files_counter_text.set("{} of {} files were decrypted".format(
            self.listbox_encrypt_files.size(), self.listbox_encrypt_files.size()))
        self.label_decrypted_files_counter_text = Label(
            self.decrypt_tab, textvariable=self.label_encrypted_files_counter_text)
        self.label_decrypted_files_counter_text.grid(
            column=0, row=2, sticky=E+W)

        button_decrypt_files = Button(
            self.decrypt_tab, text="Decrypt", command=self.buttonDecryptionClick)
        button_decrypt_files.grid(
            column=0, row=3, padx='5', pady='5', sticky=E+W)