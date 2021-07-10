from GUI.MainWindow import *
from tkinter import *

window = Tk()
window.title("Super duper Titel")
window.geometry("500x500")
window.config(background="black")
gui = GUI(window)
gui.pack(fill="both", expand=True)

mainloop()
