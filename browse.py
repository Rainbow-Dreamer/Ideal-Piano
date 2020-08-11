from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from musicpy.musicpy import read
import time

file_path = None
action = 0
track_ind_get = None
interval = None
read_result = None
sheetlen = None
set_bpm = None
off_melody = 0


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
        self.choose_track_ind_text.destroy()
        self.choose_track_ind.destroy()
        self.from_text.destroy()
        self.interval_from.destroy()
        self.to_text.destroy()
        self.interval_to.destroy()
        self.out_of_index.destroy()
        self.check_bpm_text.destroy()
        self.check_bpm.destroy()
        self.merge_all_tracks.destroy()
        self.make_button()

    def go_back(self):
        global action
        action = 1
        self.destroy()

    def quit_normal(self):
        global track_ind_get
        global interval
        global read_result
        global sheetlen
        global set_bpm
        global off_melody
        global if_merge
        if self.out_of_index.place_info():
            self.out_of_index.place_forget()
        if self.no_notes1.place_info():
            self.no_notes1.place_forget()
        set_bpm = self.check_bpm.get()
        off_melody = self.if_melody.get()
        if_merge = self.if_merge_all_tracks.get()
        try:
            track_ind_get = int(self.choose_track_ind.get())
        except:
            pass
        try:
            interval = (int(self.interval_from.get()),
                        int(self.interval_to.get()))
        except:
            pass
        try:
            if track_ind_get is not None:
                read_mode = ''
            else:
                read_mode = 'find'
            if not if_merge:
                read_result = read(file_path, track_ind_get, read_mode)
            else:
                all_tracks = read(file_path, track_ind_get, 'all')
                start_time_ls = [j[2] for j in all_tracks]
                first_track_ind = start_time_ls.index(min(start_time_ls))
                all_tracks.insert(0, all_tracks.pop(first_track_ind))
                first_track = all_tracks[0]
                all_track_notes = first_track[1]
                for i in all_tracks[1:]:
                    all_track_notes &= (i[1], i[2])
                read_result = first_track[0], all_track_notes, first_track[2]

        except Exception as e:
            print(str(e))
            read_result = 'error'

        if read_result != 'error':
            sheetlen = len(read_result[1])
            if sheetlen == 0:
                self.no_notes1.place(x=-50, y=160, width=200, height=20)
            else:
                self.destroy()
        else:
            self.out_of_index.place(x=-50, y=160, width=200, height=20)

    def make_error_labels(self):
        self.no_notes1 = ttk.Label(self.labelFrame,
                                   text='this track has no music notes')
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
            self.from_text = ttk.Label(self.labelFrame, text='from')
            self.from_text.grid(row=6, column=0)
            self.interval_from = ttk.Entry(self.labelFrame, width=5)
            self.interval_from.grid(row=6, column=1)
            self.to_text = ttk.Label(self.labelFrame, text='to')
            self.to_text.grid(row=6, column=2)
            self.interval_to = ttk.Entry(self.labelFrame, width=5)
            self.interval_to.grid(row=6, column=3)
            self.check_bpm_text = ttk.Label(self.labelFrame, text='BPM')
            self.check_bpm_text.grid(row=7, column=0)
            self.check_bpm = ttk.Entry(self.labelFrame, width=5)
            self.check_bpm.grid(row=7, column=1)
            self.if_melody = IntVar()
            self.main_melody = ttk.Checkbutton(
                self.labelFrame,
                text='main melody off when show chords',
                variable=self.if_melody)
            self.main_melody.place(x=0, y=180, width=230, height=30)
            self.if_merge_all_tracks = IntVar()
            self.merge_all_tracks = ttk.Checkbutton(
                self.labelFrame,
                text='merge all tracks',
                variable=self.if_merge_all_tracks)
            self.merge_all_tracks.place(x=100, y=0, width=200, height=30)
            self.make_error_labels()


appears = False


def setup():
    global appears
    if not appears:
        appears = True
        root = Root()
        root.mainloop()