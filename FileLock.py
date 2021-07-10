from Model.encrypter import encrypter
from GUI.MainWindow import *
from tkinter import *

#pw = "Mein PW"
#data = bytearray("Meine Bytes", encoding="UTF-8")
#crypt = encrypter()

#crypted = crypt.encrypt(data, pw)
# print(crypted)

#decrypted = crypt.decrypt(crypted, pw)
# print(decrypted)
# print(data)

window = Tk()
window.title("Super duper Titel")
window.geometry("500x500")
window.config(background="black")
gui = GUI(window)
gui.pack(fill="both", expand=True)

mainloop()
