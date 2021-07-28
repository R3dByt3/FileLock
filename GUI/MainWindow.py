from Model.filemodel import file_model
import tkinter.messagebox
from Encryption.crypto import encrypter
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilenames
from GUI.ContextMenuListBox import ContextMenuListBox
from tkinter import ttk
from os.path import *
from os import path

class MainWindow():
    __crypter: encrypter = None
    __decrypt_files: list[file_model] = []

    def __init__(self, crypter: encrypter):
        self.root = Tk()
        self.root.wm_title("FileLock")
        self.set_geometry_main_window()
        icon_path = join(dirname(dirname(realpath(__file__))),"Images", "applicationicon.ico")
        self.root.iconbitmap(icon_path)

        self.__crypter = crypter

        self.tab_control = ttk.Notebook(self.root)

        self.encrypt_tab = Frame(self.tab_control)
        self.decrypt_tab = Frame(self.tab_control)

        self.init_encrypt_tab()
        self.init_decrypt_tab()

        self.tab_control.add(self.encrypt_tab, text='Encrypt')
        self.tab_control.add(self.decrypt_tab, text='Decrypt')

        self.tab_control.pack(expand=1, fill="both")

    def set_geometry_main_window(self):
        application_width = 500
        frame_width = self.root.winfo_rootx() - self.root.winfo_x()
        window_width = application_width + 2 * frame_width

        application_height = 500
        titlebar_height = self.root.winfo_rooty() - self.root.winfo_y()
        window_height = application_height + titlebar_height + frame_width

        x = self.root.winfo_screenwidth() // 2 - window_width // 2
        y = self.root.winfo_screenheight() // 2 - window_height // 2
        self.root.geometry('{}x{}+{}+{}'.format(application_width, application_height, x, y))

    def start(self):
        self.root.mainloop()

    def get_encrypted_files(self):
        self.__decrypt_files = list(self.__crypter.read_files())
        for element in self.__decrypt_files:
            self.listbox_decrypt_files.insert("end", element.FullPath)

    def open_file_dialog(self):
        filenames = askopenfilenames()
        for element in filenames:
            self.listbox_encrypt_files.insert("end", element)

    def button_encryption_click(self):
        selected_items = self.listbox_encrypt_files.curselection()

        if len(selected_items) == 0:
            tkinter.messagebox.showerror("Encryption failed", "No files selected.")
            return

        counter = 0
        simple_mode = True

        if self.encryption_type_combobox.current() == 1:
            simple_mode = False

        for selected_item in selected_items:
            try:
                if simple_mode:
                    self.__crypter.encrypt(file_model(self.listbox_encrypt_files.get(selected_item), -1))
                else:
                    self.__crypter.encrypt2(file_model(self.listbox_encrypt_files.get(selected_item), -1))
            except Exception:
                tkinter.messagebox.showerror("Encryption failed", "The encryption failed.")
                return

            counter = counter + 1
            self.label_encrypted_files_counter_text.set("{} of {} files were encrypted".format(counter, len(selected_items)))
            self.listbox_encrypt_files.update()

        tkinter.messagebox.showinfo("Encryption succeeded", "All files were encrypted.")
        
        self.get_encrypted_files()

    def button_decryption_click(self):
        selected_items = self.listbox_decrypt_files.curselection()

        if len(selected_items) == 0:
            tkinter.messagebox.showerror("Decryption failed", "No files selected.")
            return

        counter = 0
        save_directory = askdirectory()

        for selected_item in selected_items:
            selected_file_model = next((x for x in self.__decrypt_files if x.FullPath == self.listbox_decrypt_files.get(selected_item)), None)

            try:
                if selected_file_model.EncryptionType == 1:
                    data = self.__crypter.decrypt(selected_file_model)
                else:
                    data = self.__crypter.decrypt2(selected_file_model)

                fileName = path.basename(selected_file_model.FullPath)
                combinedPath = join(save_directory, fileName)

                self.__crypter.write_bytes_to_new_file(combinedPath, data)
                
            except Exception:
                tkinter.messagebox.showerror("Decryption failed", "The decryption failed.")
                return                

            counter = counter + 1
            self.label_decrypted_files_counter_text.set("{} of {} files were decrypted".format(counter, len(selected_items)))
            self.listbox_decrypt_files.update()

        tkinter.messagebox.showinfo("Decryption succeeded", "All files were decrypted.")

    def init_encrypt_tab(self):
        Grid.columnconfigure(self.encrypt_tab, 0, weight=1)
        Grid.columnconfigure(self.encrypt_tab, 1, weight=1)

        Grid.rowconfigure(self.encrypt_tab, 0, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 1, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 2, weight=1)
        Grid.rowconfigure(self.encrypt_tab, 3, weight=0)
        Grid.rowconfigure(self.encrypt_tab, 4, weight=0)

        label_select_files = Label(self.encrypt_tab, text="Select the files you want to encrypt: ")
        label_select_files.grid(column=0, row=0, padx='5', pady='5', sticky=W)

        button_open_file_explorer = Button(self.encrypt_tab, text="Open file explorer", command=self.open_file_dialog)
        button_open_file_explorer.grid(column=1, row=0, padx='5', pady='5', sticky=E+W)

        self.encryption_type_combobox = ttk.Combobox(self.encrypt_tab, state="readonly", values=["Simple", "Extended (Needs more storage)"])
        self.encryption_type_combobox.grid(column=0, columnspan=2, row=1, padx=5, pady=5, sticky=E+W)
        self.encryption_type_combobox.current(0)

        self.listbox_encrypt_files = ContextMenuListBox(self.encrypt_tab, selectmode='multiple')
        self.listbox_encrypt_files.grid(column=0, columnspan=2, row=2, padx='5', pady='5', sticky=N+E+S+W)
        self.listbox_encrypt_files.configure(selectbackground="dimgray")

        scrollbar = Scrollbar(self.listbox_encrypt_files, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_encrypt_files.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_encrypt_files.yview)

        self.label_encrypted_files_counter_text = StringVar()
        self.label_encrypted_files_counter_text.set("")
        self.label_encrypted_files_counter = Label(self.encrypt_tab, textvariable=self.label_encrypted_files_counter_text)
        self.label_encrypted_files_counter.grid(column=0, columnspan=2, row=3, sticky=E+W)

        button_encrypt_files = Button(self.encrypt_tab, text="Encrypt", command=self.button_encryption_click)
        button_encrypt_files.grid(column=0, columnspan=2, row=4, padx='5', pady='5', sticky=E+W)

    def init_decrypt_tab(self):
        Grid.columnconfigure(self.decrypt_tab, 0, weight=1)

        Grid.rowconfigure(self.decrypt_tab, 0, weight=0)
        Grid.rowconfigure(self.decrypt_tab, 1, weight=1)
        Grid.rowconfigure(self.decrypt_tab, 2, weight=0)
        Grid.rowconfigure(self.decrypt_tab, 3, weight=0)

        label_select_files_decrypt = Label(self.decrypt_tab, text="Select the files you want to decrypt: ")
        label_select_files_decrypt.grid(column=0, row=0, padx='5', pady='5', sticky=W)

        self.listbox_decrypt_files = Listbox(self.decrypt_tab, selectmode='multiple')
        self.listbox_decrypt_files.grid(column=0, row=1, padx='5', pady='5', sticky=N+E+S+W)
        self.listbox_decrypt_files.configure(selectbackground="dimgray")

        self.get_encrypted_files()

        scrollbar = Scrollbar(self.listbox_decrypt_files, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox_decrypt_files.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_decrypt_files.yview)

        self.label_decrypted_files_counter_text = StringVar()
        self.label_decrypted_files_counter_text.set("")
        self.label_decrypted_files_counter = Label(self.decrypt_tab, textvariable=self.label_decrypted_files_counter_text)
        self.label_decrypted_files_counter.grid(column=0, row=2, sticky=E+W)

        button_decrypt_files = Button(self.decrypt_tab, text="Decrypt", command=self.button_decryption_click)
        button_decrypt_files.grid(column=0, row=3, padx='5', pady='5', sticky=E+W)