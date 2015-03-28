from __future__ import division
import Tkinter as tk
import threading
import Queue
import ttk
import time
import os, glob, datetime
import Image, ImageTk

os.chdir("C:\\Users\\sbf\\Desktop\\frames")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.queue = Queue.Queue()

        self.start = tk.Button(self, text="start", command = self.spawnthread)
        self.start.pack()
        #build a new window to display images, and load img_1.jpg
        self.level = tk.Toplevel(self)
        self.frame = tk.Frame(self.level)
        self.img = Image.open("img_11168.jpg")
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.image = tk.Label(self.frame, image = self.tkimg)
        #pack the widgets
        self.frame.pack()
        self.image.pack()
    def spawnthread(self):
        #start thread
        self.thread = ThreadedClient(self.queue)
        self.thread.start()
        #check the queue periodically
        self.periodiccall()
    def periodiccall(self):
        self.img_count = self.checkqueue()
        #update image if it's time for next image
        if self.img_count != None:
            print self.img_count
            self.update_img()
        if self.thread.is_alive():
            self.after(30, self.periodiccall)
    def update_img(self):
        self.imgname = "img_%d.jpg" %(self.img_count + 11167)
        self.img = Image.open(self.imgname)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.image.configure(image=self.tkimg)
    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                return msg
            except Queue.Empty:
                pass


class ThreadedClient(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        ct1 = datetime.datetime.now()
        ct2 = ct1
        timediff = datetime.timedelta(seconds = 0.05)
        for x in range(1,26):
            while ct2-ct1 < timediff:
                ct2 = datetime.datetime.now()
            msg = x
            #print "t",x
            self.queue.put(msg)
            ct1 = ct2


app = App()
app.mainloop()