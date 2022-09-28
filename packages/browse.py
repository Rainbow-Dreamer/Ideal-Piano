import musicpy as mp
import os
import sys
import json_module
import importlib
from PyQt5 import QtGui, QtWidgets
from change_settings import change_parameter

piano_config_path = 'packages/piano_config.json'
piano_config = json_module.json_module(piano_config_path)


def set_font(font, dpi):
    if dpi != 96.0:
        font.setPointSize(font.pointSize() * (96.0 / dpi))
    return font


class Dialog(QtWidgets.QMainWindow):

    def __init__(self, caption, directory, filter):
        super().__init__()
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            self, caption=caption, directory=directory, filter=filter)


class browse_window(QtWidgets.QMainWindow):

    def __init__(self, parent, browse_dict, file_name=None, dpi=None):
        super().__init__()
        self.parent = parent
        self.browse_dict = browse_dict
        self.dpi = dpi
        self.setWindowTitle(self.browse_dict['choose'])
        self.setMinimumSize(600, 420)

        if sys.platform == 'win32':
            self.setWindowIcon(QtGui.QIcon('resources/piano.ico'))
        elif sys.platform == 'linux':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.png'))
        elif sys.platform == 'darwin':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.icns'))
        self.labelFrame = QtWidgets.QGroupBox(self)
        self.labelFrame.setTitle(self.browse_dict['MIDI files'])
        self.labelFrame.resize(400, 320)
        self.labelFrame.move(100, 70)
        self.labelFrame.setFont(set_font(QtGui.QFont('Consolas', 12),
                                         self.dpi))
        self.go_back_button = QtWidgets.QPushButton(
            parent=self.labelFrame, text=self.browse_dict['go back'])
        self.go_back_button.clicked.connect(self.go_back)
        self.go_back_button.setFixedWidth(90)
        self.go_back_button.move(155, 60)
        self.choose_midi_file_button = QtWidgets.QPushButton(
            parent=self.labelFrame, text=self.browse_dict['choose MIDI file'])
        self.choose_midi_file_button.clicked.connect(self.fileDialog)
        self.choose_midi_file_button.setFixedWidth(200)
        self.choose_midi_file_button.move(100, 100)
        self.msg_label = QtWidgets.QLabel(parent=self.labelFrame)
        self.msg_label.setFont(set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.msg_label.resize(500, 50)
        self.msg_label.move(30, 265)
        self.show()
        if file_name:
            self.fileDialog(file_name=file_name)

    def make_button(self):
        self.choose_midi_file_button = QtWidgets.QPushButton(
            parent=self.labelFrame, text=self.browse_dict['choose MIDI file'])
        self.choose_midi_file_button.clicked.connect(self.fileDialog)
        self.choose_midi_file_button.setFixedWidth(200)
        self.choose_midi_file_button.move(100, 100)
        self.choose_midi_file_button.show()

    def redo(self):
        self.quit_normal_button.deleteLater()
        self.cancel_button.deleteLater()
        self.choose_track_ind_text.deleteLater()
        self.choose_track_ind.deleteLater()
        self.check_bpm_text.deleteLater()
        self.check_bpm.deleteLater()
        self.show_main_melody.deleteLater()
        self.show_chord.deleteLater()
        self.merge_all_tracks.deleteLater()
        self.filename_label.deleteLater()
        self.make_button()

    def go_back(self):
        self.parent.action = 1
        self.close()

    def quit_normal(self):
        self.msg_label.setText('')
        self.parent.set_bpm = self.check_bpm.text()
        if self.show_main_melody.isChecked():
            self.parent.show_mode = 1
        elif self.show_chord.isChecked():
            self.parent.show_mode = 2
        self.parent.if_merge = self.merge_all_tracks.isChecked()
        try:
            self.parent.track_ind_get = int(self.choose_track_ind.text())
        except:
            pass
        try:
            try:
                all_tracks = mp.read(self.parent.file_path,
                                     get_off_drums=False)
                if len(all_tracks) == 1:
                    if piano_config.get_off_drums and any(
                            i.channel == 9 for i in all_tracks.tracks[0]):
                        all_tracks = mp.read(self.parent.file_path,
                                             get_off_drums=False,
                                             split_channels=True)
            except:
                all_tracks = mp.read(self.parent.file_path,
                                     get_off_drums=False,
                                     split_channels=True)
            all_tracks.normalize_tempo()
            current_bpm = all_tracks.bpm
            i = 0
            while i < len(all_tracks):
                current_track = all_tracks.tracks[i]
                if all(not isinstance(k, mp.note) for k in current_track):
                    del all_tracks[i]
                    continue
                i += 1
            actual_start_time = min(all_tracks.start_times)
            drum_tracks = []
            if piano_config.get_off_drums:
                while 9 in all_tracks.channels:
                    current_drum_track_ind = all_tracks.channels.index(9)
                    drum_tracks.append(all_tracks[current_drum_track_ind])
                    del all_tracks[current_drum_track_ind]
            if not self.parent.if_merge:
                if self.parent.track_ind_get is not None:
                    all_tracks = [
                        (all_tracks.tracks[self.parent.track_ind_get],
                         current_bpm,
                         all_tracks.start_times[self.parent.track_ind_get])
                    ]
                else:
                    all_tracks = [(all_tracks.tracks[0], current_bpm,
                                   all_tracks.start_times[0])]
                all_tracks[0][0].reset_track(0)
            else:
                all_tracks = [(all_tracks.tracks[i], current_bpm,
                               all_tracks.start_times[i])
                              for i in range(len(all_tracks.tracks))]

            pitch_bends = mp.concat(
                [i[0].split(mp.pitch_bend, get_time=True) for i in all_tracks])
            for each in all_tracks:
                each[0].clear_pitch_bend('all')
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
                            while (colors == (255, 255, 255)) or (current_color
                                                                  in colors):
                                current_color = tuple(
                                    [random.randint(0, 255) for j in range(3)])
                            colors.append(current_color)
            first_track = all_tracks[0]
            all_track_notes, tempo, first_track_start_time = first_track
            for i in range(len(all_tracks)):
                current = all_tracks[i]
                current_track = current[0]
                if piano_config.use_track_colors:
                    current_color = colors[i]
                    for each in current_track:
                        each.own_color = current_color
                if i > 0:
                    all_track_notes &= (current_track,
                                        current[2] - first_track_start_time)
            all_track_notes += pitch_bends
            if self.parent.set_bpm != '':
                tempo = float(self.parent.set_bpm)
            first_track_start_time += all_track_notes.start_time
            self.parent.read_result = all_track_notes, tempo, first_track_start_time, actual_start_time, drum_tracks

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            self.parent.read_result = 'error'

        if self.parent.read_result != 'error':
            self.parent.sheetlen = len(self.parent.read_result[0])
            self.close()
        else:
            self.msg_label.setText(self.browse_dict['out of index'])

    def fileDialog(self, file_name=None):
        last_path = ''
        if file_name:
            self.filename = file_name
        else:
            if os.path.exists('last_path.txt'):
                with open('last_path.txt', encoding='utf-8') as f:
                    last_path = f.read()
            self.filename = Dialog(
                caption=self.browse_dict['choose MIDI file'],
                directory=last_path,
                filter='MIDI files (*.mid);; all files (*)').filename[0]
        if '.mid' in self.filename or '.MID' in self.filename:
            current_path = os.path.dirname(self.filename)
            if current_path != last_path:
                with open('last_path.txt', 'w', encoding='utf-8') as f:
                    f.write(current_path)
            self.parent.file_path = self.filename
            self.choose_midi_file_button.deleteLater()
            self.quit_normal_button = QtWidgets.QPushButton(
                parent=self.labelFrame, text="OK")
            self.quit_normal_button.clicked.connect(self.quit_normal)
            self.quit_normal_button.setFixedWidth(90)
            self.quit_normal_button.move(155, 100)
            self.cancel_button = QtWidgets.QPushButton(
                parent=self.labelFrame, text=self.browse_dict['cancel'])
            self.cancel_button.clicked.connect(self.redo)
            self.cancel_button.setFixedWidth(90)
            self.cancel_button.move(155, 140)
            self.quit_normal_button.show()
            self.cancel_button.show()
            current_filename = os.path.basename(self.parent.file_path)
            self.filename_label = QtWidgets.QLabel(
                parent=self,
                text=f'{self.browse_dict["file name"]}: {current_filename}')
            self.filename_label.resize(500, 50)
            self.filename_label.move(50, 20)
            self.filename_label.show()

            self.choose_track_ind_text = QtWidgets.QLabel(
                parent=self.labelFrame, text=self.browse_dict['trackind'])
            self.choose_track_ind_text.setFont(
                set_font(QtGui.QFont('Consolas', 10), self.dpi))
            self.choose_track_ind_text.move(100, 182)
            self.choose_track_ind_text.show()
            self.choose_track_ind = QtWidgets.QLineEdit(parent=self.labelFrame)
            self.choose_track_ind.setMaximumWidth(50)
            self.choose_track_ind.move(240, 180)
            self.choose_track_ind.show()
            self.check_bpm_text = QtWidgets.QLabel(parent=self.labelFrame,
                                                   text='BPM')
            self.check_bpm_text.move(155, 215)
            self.check_bpm_text.show()
            self.check_bpm = QtWidgets.QLineEdit(parent=self.labelFrame)
            self.check_bpm.setMaximumWidth(100)
            self.check_bpm.move(240, 215)
            self.check_bpm.show()
            self.show_main_melody = QtWidgets.QCheckBox(
                parent=self.labelFrame, text=self.browse_dict['show melody'])
            self.show_main_melody.clicked.connect(
                lambda: self.show_mode_check(0))
            self.show_main_melody.move(50, 250)
            self.show_main_melody.setFont(
                set_font(QtGui.QFont('Consolas', 10), self.dpi))
            self.show_main_melody.show()
            self.show_chord = QtWidgets.QCheckBox(
                parent=self.labelFrame, text=self.browse_dict['show chord'])
            self.show_chord.clicked.connect(lambda: self.show_mode_check(1))
            self.show_chord.move(200, 250)
            self.show_chord.setFont(
                set_font(QtGui.QFont('Consolas', 10), self.dpi))
            self.show_chord.show()
            self.merge_all_tracks = QtWidgets.QCheckBox(
                parent=self.labelFrame, text=self.browse_dict['merge'])
            self.merge_all_tracks.setFont(
                set_font(QtGui.QFont('Consolas', 10), self.dpi))
            self.merge_all_tracks.move(250, 65)
            self.merge_all_tracks.setChecked(True)
            self.merge_all_tracks.show()

    def show_mode_check(self, mode=0):
        if mode == 0:
            if self.show_chord.isChecked():
                self.show_chord.setChecked(False)
        elif mode == 1:
            if self.show_main_melody.isChecked():
                self.show_main_melody.setChecked(False)


class setup:

    def __init__(self, browse_dict, file_name=None):
        global piano_config
        piano_config = json_module.json_module(piano_config_path)
        self.file_path = None
        self.action = 0
        self.track_ind_get = None
        self.read_result = None
        self.sheetlen = None
        self.set_bpm = None
        self.show_mode = 0
        self.if_merge = True
        app = QtWidgets.QApplication(sys.argv)
        dpi = (app.screens()[0]).logicalDotsPerInch()
        self.current_browse_window = browse_window(self,
                                                   browse_dict,
                                                   file_name=file_name,
                                                   dpi=dpi)
        app.exec()


class midi_keyboard_window(QtWidgets.QMainWindow):

    def __init__(self, dpi=None):
        super().__init__()
        self.dpi = dpi
        self.setWindowTitle('Choose MIDI Device')
        self.setMinimumSize(800, 400)

        if sys.platform == 'win32':
            self.setWindowIcon(QtGui.QIcon('resources/piano.ico'))
        elif sys.platform == 'linux':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.png'))
        elif sys.platform == 'darwin':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.icns'))
        import pygame.midi
        pygame.midi.quit()
        pygame.midi.init()
        midi_info = []
        counter = 0
        while True:
            current = counter, pygame.midi.get_device_info(counter)
            counter += 1
            if current[1] is None:
                break
            midi_info.append(current)

        self.midi_inputs = [
            (i[0], f'{i[1][0].decode("utf-8")}, {i[1][1].decode("utf-8")}')
            for i in midi_info if i[1][2] == 1
        ]
        self.midi_outputs = [
            (i[0], f'{i[1][0].decode("utf-8")}, {i[1][1].decode("utf-8")}')
            for i in midi_info if i[1][2] == 0
        ]
        self.midi_ports = self.midi_inputs + self.midi_outputs
        self.midi_input_box = QtWidgets.QComboBox(self)
        self.midi_input_box.setFixedWidth(400)
        self.midi_input_box.addItems([i[1] for i in self.midi_inputs])
        self.midi_input_box.move(200, 70)
        self.midi_input_box.activated.connect(self.change_midi_device_id)
        self.midi_input_label = QtWidgets.QLabel(self,
                                                 text='MIDI Input Driver')
        self.midi_input_label.setFont(
            set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.midi_input_label.setFixedWidth(150)
        self.midi_input_label.move(50, 70)
        self.midi_output_box = QtWidgets.QComboBox(self)
        self.midi_output_box.setFixedWidth(400)
        self.midi_output_box.addItems([i[1] for i in self.midi_outputs])
        self.midi_output_box.move(200, 170)
        self.midi_output_label = QtWidgets.QLabel(self,
                                                  text='MIDI Output Driver')
        self.midi_output_label.setFont(
            set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.midi_output_label.setFixedWidth(150)
        self.midi_output_label.move(50, 170)
        self.msg_label = QtWidgets.QLabel(
            self,
            text=
            'Instruction: Choose your MIDI device in MIDI Input Driver box,\n             and then you can close this window.'
        )
        self.msg_label.setFont(set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.msg_label.setFixedWidth(600)
        self.msg_label.move(50, 270)
        self.show()

    def change_midi_device_id(self):
        current_midi_input = self.midi_input_box.currentText()
        current_midi_device_id = self.midi_inputs[[
            i[1] for i in self.midi_inputs
        ].index(current_midi_input)][0]
        try:
            change_parameter('midi_device_id', current_midi_device_id,
                             piano_config_path)
        except:
            import traceback
            print(traceback.format_exc())
