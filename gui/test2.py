import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import os, glob, datetime, math
import threading

#os.chdir("c:/users/sbf/desktop/images")

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        tk.Button(self, text = "open frame folder", command = self.askdir).pack()
        tk.Label(self, text = "enter glob").pack()
        self.globentry = tk.Entry(self)
        self.globentry.pack()
        self.globentry.insert(0, "*[!seg].jpg")
        self.form = tk.Entry(self)
        self.form.pack()
        self.form.insert(0, "img_?.jpg")
    
    def askdir(self):
        #self.file_path = tk.filedialog.askdirectory()
        self.file_path = "c:/users/sbf/desktop/images2"
        os.chdir(self.file_path)
        self.initialize()
    
    def initialize(self):
        self.win = tk.Toplevel()
        self.frame = tk.Frame(self.win)
        
        self.imagenames = glob.glob(self.globentry.get())
        self.reorder_names()

        self.ii = 0
        self.bufsize = 150
        self.buffer = [None]*len(self.imagenames)
        self.totalskips = 0
        self.viewskips = 0

        self.spf = 1/30
        self.num_images = len(self.buffer)
        self.flag_play = False
        self.frametime = False
        
        img = Image.open(self.imagenames[self.ii])
        self.imwidth, self.imheight = img.size
        self.tkimg = ImageTk.PhotoImage(img)
        
        self.button1 = tk.Button(self.frame, text="printbuffer", command = self.printbuffer)
        self.button2 = tk.Button(self.frame, text="play", command = self.start_play)
        self.button3 = tk.Button(self.frame, text="stop", command = self.stop_play)
        
        self.canvas = tk.Canvas(self.frame, width = self.imwidth, height = self.imheight)
        self.cimg = self.canvas.create_image(0, 0, image = self.tkimg , anchor = tk.NW)
        self.canvas.configure(highlightthickness=0)
        
        t = threading.Thread(target=self.fillbuffer)
        t.start()
        
        self.nextii()
        
        self.frame.pack()
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.canvas.pack()
    
    def reorder_names(self):
        form = self.form.get()
        ff = form.split("?")
        #print(ff)
        results = []
        for i,val in enumerate(self.imagenames):
            _,_,rest = val.partition(ff[0])
            result,_,_ = rest.partition(ff[1])
            results.append(int(result))
        sresult = sorted(range(len(results)), key=lambda k: results[k])
        names = [self.imagenames[i] for i in sresult]
        self.imagenames = names

    
    def stop_play(self):
        self.flag_play = False
        self.frametime = False
    
    def start_play(self):
        self.flag_play = True
        
    def nextii(self):
        if self.flag_play == True:
            if not self.frametime:
                self.frametime = datetime.datetime.now()
            timenow = datetime.datetime.now()
            toadd = math.floor((timenow - self.frametime).total_seconds() / self.spf)
            if toadd >= 1:
                if toadd > 5:
                    print(toadd)
                self.viewskips += 1
                self.ii += toadd
                if self.ii >= self.num_images - 1:
                    print("starting over")
                    self.ii = 0
                self.frametime = datetime.datetime.now()
                self.showimage()
            else:
                self.totalskips += 1
        self.after(1, self.nextii)
    
    def showimage(self):
        if self.buffer[self.ii] != None:
            self.canvas.itemconfig(self.cimg, image = self.buffer[self.ii])
        else:
            print("image not ready")
            self.after(10, self.showimage)
        
    def printbuffer(self):
        print(self.buffer.count(None))
        #print(self.buffer[self.ii-self.bufsize-3:self.ii+self.bufsize+3])
        print("====================")
        print(self.totalskips/self.viewskips)
        print("====================")
        
    def fillbuffer(self):
        while True:
            for i,val in enumerate(self.buffer):
                if abs(self.ii - i) < self.bufsize:
                    if self.buffer[i] == None:
                        img = Image.open(self.imagenames[i])
                        tkimg = ImageTk.PhotoImage(img)
                        self.buffer[i] = tkimg
                else:
                    self.buffer[i] = None
    


app = App()
app.mainloop()
