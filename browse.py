from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from musicpy.musicpy import read
import time

file_path = None
action = 0
track_get = 1
track_ind_get = 1
interval = None
read_result = None
sheetlen = None


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Choose Midi Files")
        self.minsize(200, 300)
        self.wm_iconbitmap('piano.ico')

        self.labelFrame = ttk.LabelFrame(self,
                                         text="midi files",
                                         borderwidth=60)
        self.labelFrame.grid(padx=200, pady=100, row=0)
        self.button_a = ttk.Button(self.labelFrame,
                                   text="Go Back",
                                   command=self.go_back)
        self.button_a.grid(row=1, column=0)

        self.make_button()
        try:
            with open('browse memory.txt') as f:
                self.last_place = f.read()
        except:
            self.last_place = "/"

    def make_button(self):
        self.button = ttk.Button(self.labelFrame,
                                 text="Choose A Midi File",
                                 command=self.fileDialog)
        self.button.grid(row=2, column=0)

    def redo(self):
        self.button.destroy()
        self.button2.destroy()
        self.no_notes1.destroy()
        self.no_notes2.destroy()
        self.choose_track_ind_text.destroy()
        self.choose_track_ind.destroy()
        self.choose_track_text.destroy()
        self.choose_track.destroy()
        self.from_text.destroy()
        self.interval_from.destroy()
        self.to_text.destroy()
        self.interval_to.destroy()
        self.make_button()

    def go_back(self):
        global action
        action = 1
        self.destroy()

    def quit_normal(self):
        global track_get
        global track_ind_get
        global interval
        global read_result
        global sheetlen
        if self.out_of_index.grid_info():
            self.out_of_index.grid_forget()
        if self.no_notes1.grid_info():
            self.no_notes1.grid_forget()
        if self.no_notes2.grid_info():
            self.no_notes2.grid_forget()

        try:
            track_get = int(self.choose_track.get())
            track_ind_get = int(self.choose_track_ind.get())
        except:
            pass
        try:
            interval = (int(self.interval_from.get()),
                        int(self.interval_to.get()))
        except:
            pass
        try:
            read_result = read(file_path, track_ind_get, track_get)
        except:
            read_result = 'error'
        if read_result != 'error':
            sheetlen = len(read_result[1])
            if sheetlen == 0:
                self.no_notes1.grid()
                self.no_notes2.grid()
            else:
                self.destroy()
        else:
            self.out_of_index.grid()

    def make_error_labels(self):
        self.no_notes1 = ttk.Label(self.labelFrame, text='this track has')
        self.no_notes2 = ttk.Label(self.labelFrame, text='mo music notes')
        self.out_of_index = ttk.Label(self.labelFrame,
                                      text='track number is out of index')

    def fileDialog(self):
        global file_path
        self.filename = filedialog.askopenfilename(
            initialdir=self.last_place,
            title="Choose A Midi File",
            filetype=(("midi files", "*.mid"), ("all files", "*.*")))
        if '.mid' in self.filename or '.MID' in self.filename:
            file_path = self.filename
            memory = self.filename[:self.filename.rindex('/') + 1]
            with open('browse memory.txt', 'w') as f:
                f.write(memory)
            self.last_place = memory
            self.button.destroy()
            self.button = ttk.Button(self.labelFrame,
                                     text="OK",
                                     command=self.quit_normal)
            self.button.grid(row=2, column=0)
            self.button2 = ttk.Button(self.labelFrame,
                                      text="CANCEL",
                                      command=self.redo)
            self.button2.grid(row=3, column=0)
            self.choose_track_ind_text = ttk.Label(self.labelFrame,
                                                   text='trackind:')
            self.choose_track_ind_text.grid(row=4, column=0)
            self.choose_track_ind = ttk.Entry(self.labelFrame, width=5)
            self.choose_track_ind.grid(row=4, column=1)
            self.choose_track_text = ttk.Label(self.labelFrame, text='track:')
            self.choose_track_text.grid(row=5, column=0)
            self.choose_track = ttk.Entry(self.labelFrame, width=5)
            self.choose_track.grid(row=5, column=1)
            self.from_text = ttk.Label(self.labelFrame, text='from')
            self.from_text.grid(row=6, column=0)
            self.interval_from = ttk.Entry(self.labelFrame, width=5)
            self.interval_from.grid(row=6, column=1)
            self.to_text = ttk.Label(self.labelFrame, text='to')
            self.to_text.grid(row=6, column=2)
            self.interval_to = ttk.Entry(self.labelFrame, width=5)
            self.interval_to.grid(row=6, column=3)
            self.make_error_labels()


def setup():
    root = Root()
    root.mainloop()