import tkinter as tk
from PIL import Image, ImageTk
import time
import os, glob, datetime, math
import scipy.io
import wave
import pyaudio

'''CHUNK = 1024

wf = wave.open("C:/Users/sbf/Google Drive/python/gui/piano2.wav")
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()'''

os.chdir("C:/Users/sbf/Desktop/images")

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.button1 = tk.Button(self, text="one", command = self.one)
        self.button2 = tk.Button(self, text="two", command = self.two)
        self.button1.pack()
        self.button2.pack()
        
        self.level = tk.Toplevel(self)
        self.frame = tk.Frame(self.level)
        self.obj = []
        self.img_count = 0
        self.spf = 1/30
        self.frametime = False
        imagenames = glob.glob("*.jpg")
        for i in imagenames:
            img = Image.open(i)
            tkimg = ImageTk.PhotoImage(img)
            self.obj.append(tkimg)

        self.num_images = len(self.obj)
        self.image = tk.Label(self.frame, image = self.obj[0])
        
        self.frame.pack()
        self.image.pack()

        self.flag = True
    def one(self):
        #print("one")
        if not self.frametime:
            self.frametime = datetime.datetime.now()

        if self.flag == True:
            timenow = datetime.datetime.now()
            toadd = math.floor((timenow - self.frametime).total_seconds() / self.spf)
            print(toadd, (timenow - self.frametime).total_seconds() / self.spf)
            if toadd >= 1:
                print("here")
                self.img_count += toadd
                if self.img_count >= self.num_images:
                    self.img_count = 0
                self.frametime = datetime.datetime.now()
                self.update_img()
        self.after(1, self.one)
        
    def two(self):
        print("two")
        self.flag = not self.flag

    def update_img(self):
        self.image.configure(image=self.obj[self.img_count])
        
app = App()
app.mainloop()

