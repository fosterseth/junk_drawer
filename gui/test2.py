import tkinter as tk
from PIL import Image, ImageTk
import time
import os, glob, datetime, math
import threading

os.chdir("c:/users/sbf/desktop/images")
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        global imglist, imgidx, imglimit, imagenames
        imgidx = 0
        imagenames = glob.glob("*.jpg")
        imglist = [0]*len(imagenames)
        imglimit = 200
        self.button1 = tk.Button(self, text="one", command = self.one)
        self.button1.pack()
        
        t = threading.Thread(target=namebuffer)
        t.start()
        
    def one(self):
        buffer[3] += 1

        
def namebuffer():
    max_idx = len(imglist)
    lower = max(0, imgidx - imglimit/2)
    upper = min(max_idx, imgidx + imglimit/2)
    
    while True:
        time.sleep(1)
        print(buffer[3])
    

    
app = App()
app.mainloop()
