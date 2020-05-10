from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfile,asksaveasfilename
import io
import os


class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
   
    def __init__(self):
        self.root = Tk()
        self.root.title("Paint")
        self.save_button = Button(self.root,text = 'Save File', command = self.save_file)
        self.save_button.grid(row=0,column=0)

        self.pen_button = Button(self.root,text = 'Clear Screen',command = self.clear_scr)
        self.pen_button.grid(row=0,column=1)
       
        self.brush_button = Button(self.root,text = 'Brush',command = self.use_brush)
        self.brush_button.grid(row=0,column=2)
       
        self.color_button = Button(self.root,text = 'Color',command = self.choose_color)
        self.color_button.grid(row=0,column=3)
       
        self.eraser_button = Button(self.root,text = 'Eraser',command = self.use_eraser)
        self.eraser_button.grid(row=0,column=4)
       
        self.choose_size_button = Scale(self.root,from_=1,to=25,orient = HORIZONTAL, sliderlength = 25)
        self.choose_size_button.grid(row=0,column=5)
       
        self.c = Canvas(self.root,bg = 'white',width=600,height=600)
        self.c.grid(row =1,columnspan = 6)
       
        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

        self.setup()
        self.root.mainloop()
       
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<ButtonRelease-1>',self.reset)
       
    def clear_scr(self):
        self.c.delete("all")
       
    def use_brush(self):
        self.activate_button(self.brush_button)
        
       
    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color = self.color)[1]
       
    def use_eraser(self):
        self.activate_button(self.eraser_button,eraser_mode = True)
   
    def activate_button(self,some_button,eraser_mode=False):
        self.active_button.config(relief= RAISED)
        some_button.config(relief = SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode
       
    def paint(self,event):
        self.line_width= self.choose_size_button.get()
        paint_color ='white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,event.x,event.y,width = self.line_width,fill = paint_color,capstyle = ROUND,smooth = TRUE,splinesteps = 36)
        self.old_x = event.x
        self.old_y = event.y
   
    def reset(self,event):
        self.old_x,self.old_y = None,None



    def save_file(self):
        fileName =asksaveasfilename(title="Save",filetypes=[('image files','*.png')],defaultextension = [('image files','*.png')])
        fName = fileName[0:(len(fileName)-4)]
        fName = fName + ".eps"
        self.c.postscript(file=fName)
        img = Image.open(fName)
        img.save(fileName, "png")
        

if __name__ == '__main__':
    Paint()

