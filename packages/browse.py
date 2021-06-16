from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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
        self.wm_iconbitmap('resources/piano.ico')

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
        self.filename_label.destroy()
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
                whole_notes = read_result[1]
                for each in whole_notes:
                    each.own_color = bar_color
                read_result[1].normalize_tempo(read_result[0],
                                               start_time=read_result[2])
                if clear_pitch_bend:
                    read_result[1].clear_pitch_bend(value=0)
            else:
                all_tracks = read(file_path,
                                  track_ind_get,
                                  'all',
                                  get_off_drums=get_off_drums)
                if not all_tracks:
                    all_tracks = read(file_path,
                                      track_ind_get,
                                      'all',
                                      get_off_drums=False,
                                      to_piece=True,
                                      split_channels=True)
                    all_tracks_new = [(all_tracks.tempo, all_tracks.tracks[i],
                                       all_tracks.start_times[i])
                                      for i in range(len(all_tracks.tracks))]
                    if get_off_drums:
                        drums_ind = all_tracks.channels.index(9)
                        if all_tracks.start_times[drums_ind] != min(
                                all_tracks.start_times):
                            del all_tracks_new[drums_ind]
                    all_tracks = all_tracks_new
                if clear_pitch_bend:
                    for each in all_tracks:
                        each[1].clear_pitch_bend(value=0)
                start_time_ls = [j[2] for j in all_tracks]
                first_track_ind = start_time_ls.index(min(start_time_ls))
                all_tracks.insert(0, all_tracks.pop(first_track_ind))
                if use_track_colors:
                    if not use_default_tracks_colors:
                        color_num = len(all_tracks)
                        import random
                        colors = []
                        for i in range(color_num):
                            current_color = tuple(
                                [random.randint(0, 255) for j in range(3)])
                            while (colors == (255, 255, 255)) or (current_color
                                                                  in colors):
                                current_color = tuple(
                                    [random.randint(0, 255) for j in range(3)])
                            colors.append(current_color)
                    else:
                        colors = tracks_colors
                first_track = all_tracks[0]
                tempo, all_track_notes, first_track_start_time = first_track
                for i in range(len(all_tracks)):
                    current = all_tracks[i]
                    current_track = current[1]
                    if use_track_colors:
                        current_color = colors[i]
                        for each in current_track:
                            each.own_color = current_color
                    if i > 0:
                        all_track_notes &= (current_track, current[2] -
                                            first_track_start_time)
                all_track_notes.normalize_tempo(
                    tempo, start_time=first_track_start_time)
                if set_bpm != '':
                    tempo = float(set_bpm)
                read_result = tempo, all_track_notes, first_track_start_time

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
            self.merge_all_tracks.place(x=100, y=0, width=125, height=30)
            self.make_error_labels()
            current_filename = os.path.basename(file_path)
            self.filename_label = ttk.Label(
                self, text=f'file name: {current_filename}')
            self.filename_label.place(x=60, y=50, width=2000, height=30)


appears = False


def setup():
    global appears
    if not appears:
        appears = True
        root = Root()
        root.mainloop()