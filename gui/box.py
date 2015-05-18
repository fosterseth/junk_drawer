import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import glob
import os

class App( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )
        
        #self.tmp = tk.Label(text = "Please open directory where image files are location").pack()
        file_path = filedialog.askdirectory()
        #file_path = "C:/Users/sbf/Desktop/images"
        os.chdir(file_path)
        #self.tmp.pack_forget()
        
        self.ii = 0
        self.imagenames = glob.glob( "*.jpg" )
        self.data = (len(self.imagenames))*[None]
        img = Image.open( self.imagenames[self.ii] )
        self.tkimg = ImageTk.PhotoImage( img )
        
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)
        self.canvas = tk.Canvas( self.frame2, width = 640, height = 480, bg = "blue")
        self.cimg = self.canvas.create_image( 0, 0, image = self.tkimg , anchor = tk.NW )
        self.canvas.configure(highlightthickness=0)
        self.scb = tk.Scrollbar(self.frame2, orient = tk.VERTICAL)
        self.listbox = tk.Listbox(self.frame2, width = 35, yscrollcommand=self.scb.set)
        self.save_button = tk.Button(self.frame1, text = "Save", command = self.save)
        self.save_location = None
        self.label = tk.Label(self.frame1, text = "Right Arrow: Next, Left Arrow: Prev, Right-Click: Clear")
        self.scb.config(command=self.listbox.yview)
        for i in self.imagenames:
            self.listbox.insert(tk.END, i + ", " + "None")
        
        
        self.bind("<Right>", self.next_image)
        self.bind("<Left>", self.prev_image)
        self.canvas.bind("<B1-Motion>", self.clicked)
        self.canvas.bind("<ButtonRelease-1>", self.new_rect)
        self.canvas.bind("<Button-3>", self.clear_rect)
        
        self.flag_has_rect = False
        self.flag_new_rect = False
        
        self.frame1.pack()
        self.frame2.pack()
        self.label.pack(side=tk.LEFT)
        self.save_button.pack(side = tk.RIGHT)
        self.canvas.pack(side = tk.LEFT)
        self.scb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.RIGHT, fill = tk.BOTH, expand = 1)
    def next_image(self, event):
        print("next")
        if self.ii+1 < len(self.imagenames):
            print(self.ii, len(self.imagenames)-1)
            if self.flag_has_rect:
                self.data[self.ii] = self.canvas.coords(self.rect)
                self.listbox.delete(self.ii)
                self.listbox.insert(self.ii, self.imagenames[self.ii] + ", " + "Done")
        
            self.ii += 1
            if not self.data[self.ii] ==  None:
                self.draw_stored_rect()
            img = Image.open(self.imagenames[self.ii])
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.cimg, image = self.tkimg)
        
    def prev_image(self, event):
        print("prev")
        if self.ii-1 > -1:
            print(self.ii, len(self.imagenames)-1)
            if self.flag_has_rect:
                self.data[self.ii] = self.canvas.coords(self.rect)
                self.listbox.delete(self.ii)
                self.listbox.insert(self.ii, self.imagenames[self.ii] + ", " + "Done")
        
            self.ii -= 1
            if not self.data[self.ii] ==  None:
                self.draw_stored_rect()
            img = Image.open(self.imagenames[self.ii])
            self.tkimg = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.cimg, image = self.tkimg)
        
    def clicked(self, event):
        print("xy ", event.x, event.y)
        if self.flag_new_rect and self.flag_has_rect:
            self.canvas.delete(self.rect)
            self.flag_new_rect = False
            self.flag_has_rect = False
        if not self.flag_has_rect:
            self.rect = self.canvas.create_rectangle(event.x, event.y, event.x+5, event.y+5, fill = "", outline = "blue", width = 3)
            self.flag_has_rect = True
            self.point = [event.x, event.y]
        else:
            minx = min(event.x, self.point[0])
            maxx = max(event.x, self.point[0])
            miny = min(event.y, self.point[1])
            maxy = max(event.y, self.point[1])
            print(minx,miny,maxx,maxy)
            self.canvas.coords(self.rect, minx, miny, maxx, maxy)
            
    def new_rect(self, event):
        self.flag_new_rect = True
    
    def clear_rect(self, event):
        if self.flag_has_rect:
            self.canvas.delete(self.rect)
            self.flag_has_rect = False
        
    def draw_stored_rect(self):
        print("restoring rect", self.ii)
        minx = self.data[self.ii][0]
        miny = self.data[self.ii][1]
        maxx = self.data[self.ii][2]
        maxy = self.data[self.ii][3]
        self.canvas.coords(self.rect, minx, miny, maxx, maxy)
    
    def save(self):
        if self.save_location == None:
            self.save_location = filedialog.asksaveasfilename()
        fid = open(self.save_location, "w")
        for i, val in enumerate(self.data):
            if not val == None:
                towrite = self.imagenames[i] + "," + ','.join(str(n) for n in val) + "\n"
                fid.write(towrite)
        fid.close()

app = App()
app.focus_force()
app.mainloop()
