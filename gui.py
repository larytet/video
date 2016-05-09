#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter
import ttk 
class Example(ttk.Frame):
  
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=320, height=200, borderwidth=2, relief=Tkinter.RAISED)
        self.pack_propagate(False)
        self.pack()   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
      
        self.parent.title("Absolute positioning")
        self.pack(fill=Tkinter.BOTH, expand=1)
        
        ttk.Style().configure("TFrame", background="#333")
        
        label1 = Tkinter.Label(self)
        label1.place(x=20, y=20)
        
        label2 = Tkinter.Label(self)
        label2.place(x=40, y=160)        
        
        label3 = Tkinter.Label(self)
        label3.place(x=170, y=50)        
              

def main():
  
    root = Tkinter.Tk()
    root.overrideredirect(1)
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  