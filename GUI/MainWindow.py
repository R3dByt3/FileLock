from tkinter import *
from tkinter import font
from tkinter.font import Font 
import tkinter.messagebox
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from GUI.ContextMenuListBox import ContextMenuListBox
from tkinter import ttk

class MainWindow():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("File encryptor")
        self.root.iconbitmap("Images/applicationicon.ico")
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

    def init_encrypt_tab(self):
        Grid.columnconfigure(self.encrypt_tab, 0, weight=1)
        Grid.columnconfigure(self.encrypt_tab, 1, weight=1)

        Grid.rowconfigure(self.encrypt_tab, 0, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 1, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 2, weight=1)
        Grid.rowconfigure(self.encrypt_tab, 3, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 4, weight=0)

        self.label_select_files = Label(self.encrypt_tab, text="Select the files you want to encrypt: ")
        self.label_select_files.grid(column=0, row=0, padx='5', pady='5', sticky=W)

        self.button_open_file_explorer = Button(self.encrypt_tab, text="Open file explorer", command=self.openFileDialog)
        self.button_open_file_explorer.grid(column=1, row=0, padx='5', pady='5', sticky=E+W)

        self.encryption_type_combobox = ttk.Combobox(self.encrypt_tab, state="readonly", values=["Simple", "Extended (Needs more storage)"])
        self.encryption_type_combobox.grid(column=0, columnspan=2, row=1, padx=5, pady=5, sticky=E+W)
        self.encryption_type_combobox.current(0)

        self.listbox_encrypt_files = ContextMenuListBox(self.encrypt_tab, selectmode='multiple')
        self.listbox_encrypt_files.grid(column=0, columnspan=2, row=2, padx='5', pady='5', sticky=N+E+S+W)

        self.label_encrypted_files_counter_text = StringVar()
        self.label_encrypted_files_counter_text.set("{} of {} files were encrypted".format(self.listbox_encrypt_files.size(), self.listbox_encrypt_files.size()))
        self.label_encrypted_files_counter = Label(self.encrypt_tab, textvariable=self.label_encrypted_files_counter_text)
        self.label_encrypted_files_counter.grid(column=0, columnspan=2, row=3, sticky=E+W)

        self.button_encrypt_files = Button(self.encrypt_tab, text="Encrypt", command=self.buttonEncryptionClick)
        self.button_encrypt_files.grid(column=0, columnspan=2, row=4, padx='5', pady='5', sticky=E+W)

    def init_decrypt_tab(self):
        Grid.columnconfigure(self.decrypt_tab, 0, weight=1)

        Grid.rowconfigure(self.decrypt_tab, 0, weight=0)
        Grid.rowconfigure(self.decrypt_tab, 1, weight=1)
        Grid.rowconfigure(self.decrypt_tab, 2, weight=0)
        Grid.rowconfigure(self.decrypt_tab, 3, weight=0)

        self.label_select_files_decrypt = Label(self.decrypt_tab, text="Select the files you want to decrypt: ")
        self.label_select_files_decrypt.grid(column=0, row=0, padx='5', pady='5', sticky=W)

        self.listbox_decrypt_files = Listbox(self.decrypt_tab, selectmode='multiple')
        self.listbox_decrypt_files.grid(column=0, row=1, padx='5', pady='5', sticky=N+E+S+W)

        self.label_decrypted_files_counter_text = StringVar()
        self.label_decrypted_files_counter_text.set("{} of {} files were decrypted".format(self.listbox_encrypt_files.size(), self.listbox_encrypt_files.size()))
        self.label_decrypted_files_counter_text = Label(self.decrypt_tab, textvariable=self.label_encrypted_files_counter_text)
        self.label_decrypted_files_counter_text.grid(column=0, row=2, sticky=E+W)

        self.button_decrypt_files = Button(self.decrypt_tab, text="Decrypt", command=self.buttonDecryptionClick)
        self.button_decrypt_files.grid(column=0, row=3, padx='5', pady='5', sticky=E+W)