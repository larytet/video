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
        image =Image.open("background_image.jpg.png")
        background_image = ImageTk.PhotoImage(image)
        background_image_width = background_image.width()
        background_image_height = background_image.height()
        
        background_label = Tkinter.Label(self.parent,image=background_image)
        background_label.photo=background_image
        background_label.pack()   
        self.background_label = background_label     

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = screen_width/2 - background_image_width/2
        y = screen_height/2 - background_image_height/2
        self.parent.geometry('%dx%d+%d+%d' % (background_image_width, background_image_height, x, y))

def main():
  
    root = Tkinter.Tk()
    root.overrideredirect(1)
    root.wm_attributes('-topmost', 1)
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  