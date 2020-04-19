from tkinter import *
from tkinter import ttk
from tkinter import filedialog

file_path = None
action = 0
track_get = 1
track_ind_get = 1
interval = None


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
        self.make_button()

    def go_back(self):
        global action
        action = 1
        self.destroy()

    def quit_normal(self):
        global track_get
        global track_ind_get
        global interval
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
        self.destroy()

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
                                                   text='trackind:').grid(
                                                       row=4, column=0)
            self.choose_track_ind = ttk.Entry(self.labelFrame, width=5)
            self.choose_track_ind.grid(row=4, column=1)
            self.choose_track_text = ttk.Label(self.labelFrame,
                                               text='track:').grid(row=5,
                                                                   column=0)
            self.choose_track = ttk.Entry(self.labelFrame, width=5)
            self.choose_track.grid(row=5, column=1)
            ttk.Label(self.labelFrame, text='from').grid(row=6, column=0)
            self.interval_from = ttk.Entry(self.labelFrame, width=5)
            self.interval_from.grid(row=6, column=1)
            ttk.Label(self.labelFrame, text='to').grid(row=6, column=2)
            self.interval_to = ttk.Entry(self.labelFrame, width=5)
            self.interval_to.grid(row=6, column=3)


def setup():
    root = Root()
    root.mainloop()