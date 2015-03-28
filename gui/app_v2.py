import tkinter as tk
from PIL import Image, ImageTk
import time
import os, glob, datetime, math

os.chdir("C:/Users/sbf/Desktop/images")

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.start = tk.Button(self, text="start", command = self.preplay)
        self.start.pack()
        
        self.level = tk.Toplevel(self)
        self.frame = tk.Frame(self.level)
        
        self.obj = []
        for i in range(10000, 10309):
            imgname = "img_%d.jpg" %i
            img = Image.open(imgname)
            tkimg = ImageTk.PhotoImage(img)
            self.obj.append(tkimg)
            
        self.image = tk.Label(self.frame, image = self.obj[0])
        
        self.frame.pack()
        self.image.pack()
    def preplay(self):
        self.begin = datetime.datetime.now()
        self.img_count = 10000
        self.play()
        print("here")
        
    def play(self):
        '''ct1 = datetime.datetime.now()
        ct2 = ct1
        timediff = datetime.timedelta(seconds = 0.001)
        while ct2-ct1 < timediff:
            ct2 = datetime.datetime.now()'''
        self.img_count += 1
        if self.img_count < 10010:
            self.update_img()
            self.after(1000, self.play)
        else:
            self.end = datetime.datetime.now()
    def update_img(self):
            self.imgname = "img_%d.jpg" %self.img_count
            print(self.imgname)
            self.img = Image.open(self.imgname)
            self.tkimg = ImageTk.PhotoImage(self.img)
            self.image.configure(image=self.tkimg)
app = App()
app.mainloop()
