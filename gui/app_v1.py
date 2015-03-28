from __future__ import division
import tkinter as tk
import threading
import queue
import time
import os, glob, datetime, math
from PIL import Image, ImageTk

os.chdir("C:/Users/sbf/Desktop/images")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.queue = queue.Queue()
        self.stopqueue = queue.Queue()

        #create start button
        self.start = tk.Button(self, text="start", command = self.spawnthread)
        self.start.pack()
        #create stop button
        self.stop = tk.Button(self, text="stop", command = self.stopthread)
        self.stop.pack()
        #create scroll bar
        #self.scroll = tk.Scale(self, from_=1, to=25, orient=tk.HORIZONTAL, length=600)
        #self.scroll.pack()
        #create scroll window
        #self.nav = tk.Canvas(self, width=600, height=75, background="white")
        #bind button1 command to drawing rectangles
        #self.nav.bind("<Button-1>", lambda event: self.draw_rect(event, 1))
        #self.nav.bind("<ButtonRelease-1>", lambda event: self.draw_rect(event, 2))
        #self.nav.pack()
        #build a new window to display images, and load img_1.jpg
        self.level = tk.Toplevel(self)
        self.frame = tk.Frame(self.level)
        self.img = Image.open("img_10000.jpg")
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.image = tk.Label(self.frame, image = self.tkimg)
        #pack the widgets
        self.frame.pack()
        self.image.pack()
    def spawnthread(self):
        #start thread
        self.thread = ThreadedClient(self.queue, self.stopqueue)
        self.thread.start()
        #check the queue periodically
        self.periodiccall()
    def stopthread(self):
        self.stopqueue.put("stop")
        self.img_count = 10000
        self.thread.stop()

    def periodiccall(self):
        self.img_count = self.checkqueue()
        #self.img_count = self.scroll.get()
        #update image if it's time for next image
        if self.img_count != None:
            #print(self.img_count)
            self.update_img()
            #self.scroll.set(self.img_count)
        #if self.thread.is_alive():
        self.after(1, self.periodiccall)

    def update_img(self):
        print(self.img_count)
        self.imgname = "img_%d.jpg" %self.img_count
        self.img = Image.open(self.imgname)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.image.configure(image=self.tkimg)

    def draw_rect(self, event, flag):
        if flag == 1:
            self.begin = event.x
            #ycoord = event.x+10
            self.scroll.set(math.ceil(self.begin/600*25))
            #self.nav.create_rectangle(event.x, 0, ycoord, 74, fill="red")
        elif flag == 2:
            self.end = event.x
            self.nav.create_rectangle(self.begin, 0, self.end, 74, fill="red")
    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                return msg
            except queue.Empty:
                pass


class ThreadedClient(threading.Thread):
    def __init__(self, queue, stopqueue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.stopqueue = stopqueue
    def run(self):
        ct1 = datetime.datetime.now()
        ct2 = ct1
        timediff = datetime.timedelta(seconds = 1/30)
        stop = False
        while stop == False:
            for x in range(10001,10309):
                while ct2-ct1 < timediff:
                    ct2 = datetime.datetime.now()
                msg = x
                self.queue.put(msg)
                ct1 = ct2
                try:
                    msg = self.stopqueue.get(0)
                    if msg == "stop":
                        stop = True
                        break
                except queue.Empty:
                    pass


app = App()
app.mainloop()
