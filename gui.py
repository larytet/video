#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Label, BOTH
from ttk import Frame, Style

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
      
        self.parent.title("Absolute positioning")
        self.pack(fill=BOTH, expand=1)
        
        Style().configure("TFrame", background="#333")
        
        label1 = Label(self)
        label1.place(x=20, y=20)
        
        label2 = Label(self)
        label2.place(x=40, y=160)        
        
        label3 = Label(self)
        label3.place(x=170, y=50)        
              

def main():
  
    root = Tk()
    root.geometry("300x280+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  