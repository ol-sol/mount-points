from sqlite3 import Row
from time import strftime
import tkinter as tk
import tkinter.ttk as ttk
from backend import Mounting

m = Mounting()

class Interface(object):

    def __init__(self, window):
        self.window = window
        self.window.wm_title("Mounting")

        self.tree = ttk.Treeview(window, show='tree', columns=('MP','Row'), displaycolumns=0)
        for i, mount in enumerate(m.mounts):
            parent_iid = self.tree.insert(parent='', index=i, text=mount["server"], open=True)
            for j, line in enumerate(mount["mount_points"]):
                self.tree.insert(parent=parent_iid, index=j, values=(line["mp"],line["row"]))
        self.tree.grid(row=0,column=0,rowspan=6, columnspan=2)
        self.tree.bind("<B1-Motion>",self.bMove, add='+')
        self.initial_parents = self.tree.get_children()

        b1 = tk.Button(window, text = "Save", command=self.bSave)
        b1.grid(row=0,column=3)

        b2 = tk.Button(window, text = "Sync", command=self.bSync)
        b2.grid(row=1,column=3)

        b3 = tk.Button(window, text = "Reload")
        b3.grid(row=2,column=3)

        b4 = tk.Button(window, text = "Exit", command=window.destroy)
        b4.grid(row=3,column=3)

    def bMove(self, event):
        tv = event.widget        
        moveto = tv.index(tv.identify_row(event.y))
        newparent = tv.parent(tv.identify_row(event.y))    
        for s in tv.selection():
            if s not in self.initial_parents:
                tv.move(s, newparent, moveto)

    def bSave(self):
        list_mounts = [{"server": 
                        self.tree.item(parent, "text"), 
                "mount_points": 
                        [{"mp": self.tree.item(row, "values")[0], "row": self.tree.item(row, "values")[1]} for row in self.tree.get_children(parent)]
                } for parent in self.initial_parents]
        m.save(list_mounts)

    def bSync(self):
        m.sync()


window = tk.Tk()
interface = Interface(window)
window.mainloop()