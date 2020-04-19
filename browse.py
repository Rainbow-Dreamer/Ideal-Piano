from tkinter import *
from tkinter import ttk
from tkinter import filedialog
 
file_path = None 
action = 0
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Choose Midi Files")
        self.minsize(100, 100)
        self.wm_iconbitmap('piano.ico')
 
        self.labelFrame = ttk.LabelFrame(self, text = "midi files")
        self.labelFrame.grid(column = 0, row = 1, padx = 100, pady = 100)
        self.button_a = ttk.Button(self.labelFrame, text = "Go Back",command = self.go_back)
        self.button_a.grid(column = 1, row = 0)        
 
        self.make_button()
        try:
            with open('browse memory.txt') as f:
                self.last_place = f.read()
        except:
            self.last_place = "/"
 
 
 
    def make_button(self):
        self.button = ttk.Button(self.labelFrame, text = "Choose A Midi File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
        
    def redo(self):
        self.button.destroy()
        self.button2.destroy()
        self.make_button()
    def go_back(self):
        global action
        action = 1
        self.destroy()
 
    def fileDialog(self):
        global file_path
        self.filename = filedialog.askopenfilename(initialdir = self.last_place , title = "Choose A Midi File", filetype =
        (("midi files","*.mid"),("all files","*.*")) )
        if '.mid' in self.filename or '.MID' in self.filename:
            file_path = self.filename
            memory = self.filename[:self.filename.rindex('/')+1]
            with open('browse memory.txt', 'w') as f:
                f.write(memory)
            self.last_place  = memory            
            self.button.destroy()
            self.button = ttk.Button(self.labelFrame, text = "OK",command = self.destroy)
            self.button.grid(column = 1, row = 1)
            self.button2 = ttk.Button(self.labelFrame, text = "CANCEL",command = self.redo)
            self.button2.grid(column = 1, row = 2)   
            
 
 
 
 
 
def setup():
    root = Root()
    root.mainloop()