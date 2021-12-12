import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import musicpy as mp
import os
import sys
import piano_config
import importlib


class browse_window(tk.Tk):
    def __init__(self, parent, browse_dict):
        super(browse_window, self).__init__()
        self.parent = parent
        self.browse_dict = browse_dict
        self.title(self.browse_dict['choose'])
        self.minsize(200, 300)

        if sys.platform == 'win32':
            self.wm_iconbitmap('resources/piano.ico')
        elif sys.platform == 'linux':
            self.tk.call('wm', 'iconphoto', self._w,
                         tk.PhotoImage(file='resources/piano_icon.png'))

        self.labelFrame = ttk.LabelFrame(self,
                                         text=self.browse_dict['MIDI files'],
                                         borderwidth=70)
        self.labelFrame.grid(padx=200, pady=100, row=0)
        self.button_a = ttk.Button(self.labelFrame,
                                   text=self.browse_dict['go back'],
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
                                 text=self.browse_dict['choose MIDI file'],
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
        self.parent.action = 1
        self.destroy()

    def quit_normal(self):
        if self.out_of_index.place_info():
            self.out_of_index.place_forget()
        if self.no_notes1.place_info():
            self.no_notes1.place_forget()
        self.parent.set_bpm = self.check_bpm.get()
        self.parent.off_melody = self.if_melody.get()
        self.parent.if_merge = self.if_merge_all_tracks.get()
        try:
            self.parent.track_ind_get = int(self.choose_track_ind.get())
        except:
            pass
        try:
            self.parent.interval = (int(self.interval_from.get()),
                                    int(self.interval_to.get()))
        except:
            pass
        try:
            if self.parent.track_ind_get is not None:
                read_mode = ''
            else:
                read_mode = 'find'
            if not self.parent.if_merge:
                self.parent.read_result = mp.read(self.parent.file_path,
                                                  self.parent.track_ind_get,
                                                  read_mode)
                whole_notes = self.parent.read_result[1]
                for each in whole_notes:
                    each.own_color = piano_config.bar_color
                self.parent.read_result[1].normalize_tempo(
                    self.parent.read_result[0],
                    start_time=self.parent.read_result[2])
            else:
                try:
                    all_tracks = mp.read(
                        self.parent.file_path,
                        self.parent.track_ind_get,
                        mode='all',
                        get_off_drums=piano_config.get_off_drums,
                        to_piece=True)
                except:
                    all_tracks = mp.read(
                        self.parent.file_path,
                        self.parent.track_ind_get,
                        mode='all',
                        get_off_drums=piano_config.get_off_drums,
                        to_piece=True,
                        split_channels=True)
                all_tracks.normalize_tempo()
                all_tracks = [(all_tracks.bpm, all_tracks.tracks[i],
                               all_tracks.start_times[i])
                              for i in range(len(all_tracks.tracks))]
                pitch_bends = mp.concat([
                    i[1].split(mp.pitch_bend, get_time=True)
                    for i in all_tracks
                ])
                for each in all_tracks:
                    each[1].clear_pitch_bend('all')
                start_time_ls = [j[2] for j in all_tracks]
                first_track_ind = start_time_ls.index(min(start_time_ls))
                all_tracks.insert(0, all_tracks.pop(first_track_ind))
                if piano_config.use_track_colors:
                    color_num = len(all_tracks)
                    import random
                    if not piano_config.use_default_tracks_colors:
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
                        colors = piano_config.tracks_colors
                        colors_len = len(colors)
                        if colors_len < color_num:
                            for k in range(color_num - colors_len):
                                current_color = tuple(
                                    [random.randint(0, 255) for j in range(3)])
                                while (colors
                                       == (255, 255, 255)) or (current_color
                                                               in colors):
                                    current_color = tuple([
                                        random.randint(0, 255)
                                        for j in range(3)
                                    ])
                                colors.append(current_color)
                first_track = all_tracks[0]
                tempo, all_track_notes, first_track_start_time = first_track
                for i in range(len(all_tracks)):
                    current = all_tracks[i]
                    current_track = current[1]
                    if piano_config.use_track_colors:
                        current_color = colors[i]
                        for each in current_track:
                            each.own_color = current_color
                    if i > 0:
                        all_track_notes &= (current_track, current[2] -
                                            first_track_start_time)
                all_track_notes += pitch_bends
                if self.parent.set_bpm != '':
                    tempo = float(self.parent.set_bpm)
                self.parent.read_result = tempo, all_track_notes, first_track_start_time

        except Exception as e:
            print(str(e))
            self.parent.read_result = 'error'

        if self.parent.read_result != 'error':
            self.parent.sheetlen = len(self.parent.read_result[1])
            if self.parent.sheetlen == 0:
                self.no_notes1.place(x=-50, y=160, width=200, height=20)
            else:
                self.destroy()
        else:
            self.out_of_index.place(x=-50, y=160, width=200, height=20)

    def make_error_labels(self):
        self.no_notes1 = ttk.Label(self.labelFrame,
                                   text=self.browse_dict['no notes'])
        self.out_of_index = ttk.Label(self.labelFrame,
                                      text=self.browse_dict['out of index'])

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(
            initialdir=self.last_place,
            title=self.browse_dict['choose MIDI file'],
            filetypes=(("MIDI files", "*.mid"), ("all files", "*.*")))
        if '.mid' in self.filename or '.MID' in self.filename:
            self.parent.file_path = self.filename
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
                                      text=self.browse_dict['cancel'],
                                      command=self.redo)
            self.button2.grid(row=3, column=0)
            self.choose_track_ind_text = ttk.Label(
                self.labelFrame, text=self.browse_dict['trackind'])
            self.choose_track_ind_text.grid(row=4, column=0)
            self.choose_track_ind = ttk.Entry(self.labelFrame, width=5)
            self.choose_track_ind.grid(row=4, column=1)
            self.from_text = ttk.Label(self.labelFrame,
                                       text=self.browse_dict['from'])
            self.from_text.grid(row=6, column=0)
            self.interval_from = ttk.Entry(self.labelFrame, width=5)
            self.interval_from.grid(row=6, column=1)
            self.to_text = ttk.Label(self.labelFrame,
                                     text=self.browse_dict['to'])
            self.to_text.grid(row=6, column=2)
            self.interval_to = ttk.Entry(self.labelFrame, width=5)
            self.interval_to.grid(row=6, column=3)
            self.check_bpm_text = ttk.Label(self.labelFrame, text='BPM')
            self.check_bpm_text.grid(row=7, column=0)
            self.check_bpm = ttk.Entry(self.labelFrame, width=5)
            self.check_bpm.grid(row=7, column=1)
            self.if_melody = tk.IntVar()
            self.main_melody = ttk.Checkbutton(self.labelFrame,
                                               text=self.browse_dict['melody'],
                                               variable=self.if_melody)
            self.main_melody.place(x=-60, y=180, width=300, height=30)
            self.if_merge_all_tracks = tk.IntVar()
            self.merge_all_tracks = ttk.Checkbutton(
                self.labelFrame,
                text=self.browse_dict['merge'],
                variable=self.if_merge_all_tracks)
            self.merge_all_tracks.place(x=100, y=0, width=125, height=30)
            self.make_error_labels()
            current_filename = os.path.basename(self.parent.file_path)
            self.filename_label = ttk.Label(
                self,
                text=f'{self.browse_dict["file name"]}: {current_filename}')
            self.filename_label.place(x=60, y=50, width=2000, height=30)


class setup:
    def __init__(self, browse_dict):
        importlib.reload(piano_config)
        self.file_path = None
        self.action = 0
        self.track_ind_get = None
        self.interval = None
        self.read_result = None
        self.sheetlen = None
        self.set_bpm = None
        self.off_melody = 0
        self.if_merge = False
        self.current_browse_window = browse_window(self, browse_dict)
        self.current_browse_window.mainloop()
