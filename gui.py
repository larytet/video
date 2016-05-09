#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter
import ttk 
from PIL import Image, ImageTk
class Example(ttk.Frame):
  
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=0, relief=Tkinter.RAISED)
        self.pack_propagate(False)
        self.pack()   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
      
        #self.pack(fill=Tkinter.BOTH, expand=1)
        
        image =Image.open("background_image.jpg.png")
        background_image = ImageTk.PhotoImage(image)
        w = background_image.width()
        h = background_image.height()
        self.parent.geometry('%dx%d+0+0' % (w,h))
        
        background_label = Tkinter.Label(self.parent,image=background_image)
        background_label.photo=background_image
        #background_label.place(x=0, y=0)
        background_label.pack()   
        self.background_label = background_label     


def main():
  
    root = Tkinter.Tk()
    root.overrideredirect(1)
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  