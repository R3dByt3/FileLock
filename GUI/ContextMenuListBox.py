from tkinter import *

class ContextMenuListBox(Listbox):
    def __init__(self, parent, *args, **kwargs):
        Listbox.__init__(self, parent, *args, **kwargs)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side = RIGHT)

        self.yview_scroll = scrollbar.set

        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Remove", command=self.remove_selected)

        self.bind("<Button-3>", self.popup)

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def remove_selected(self):
        for element in self.curselection()[::-1]:
            self.delete(element)
        