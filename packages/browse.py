import musicpy as mp
import os
import sys
import piano_config
import importlib
from PyQt5 import QtGui, QtWidgets


class Dialog(QtWidgets.QMainWindow):

    def __init__(self, caption, directory, filter):
        super().__init__()
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            self, caption=caption, directory=directory, filter=filter)


class browse_window(QtWidgets.QMainWindow):

    def __init__(self, parent, browse_dict, file_name=None):
        super().__init__()
        self.parent = parent
        self.browse_dict = browse_dict
        self.setWindowTitle(self.browse_dict['choose'])
        self.setMinimumSize(600, 420)

        if sys.platform == 'win32':
            self.setWindowIcon(QtGui.QIcon('resources/piano.ico'))
        elif sys.platform == 'linux':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.png'))
        elif sys.platform == 'darwin':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.icns'))
        self.browse_layout = QtWidgets.QHBoxLayout()
        self.labelFrame = QtWidgets.QGroupBox(self)
        self.labelFrame.setTitle(self.browse_dict['MIDI files'])
        self.labelFrame.resize(400, 320)
        self.labelFrame.move(100, 70)
        self.labelFrame.setFont(QtGui.QFont('Consolas', 12))
        self.browse_layout.addWidget(self.labelFrame)
        self.setLayout(self.browse_layout)
        self.go_back_button = QtWidgets.QPushButton(
            parent=self.labelFrame, text=self.browse_dict['go back'])
        self.go_back_button.clicked.connect(self.go_back)
        self.go_back_button.resize(80, 30)
        self.go_back_button.move(155, 60)
        self.choose_midi_file_button = QtWidgets.QPushButton(
            parent=self.labelFrame, text=self.browse_dict['choose MIDI file'])
        self.choose_midi_file_button.clicked.connect(self.fileDialog)
        self.choose_midi_file_button.setFixedWidth(200)
        self.choose_midi_file_button.move(100, 100)
        self.msg_label = QtWidgets.QLabel(parent=self.labelFrame)
        self.msg_label.setFont(QtGui.QFont('Consolas', 10))
        self.msg_label.resize(500, 50)
        self.msg_label.move(30, 265)
        self.show()
        if file_name:
            self.fileDialog(file_name=file_name)

    def make_button(self):
        self.choose_midi_file_button = QtWidgets.QPushButton(
            parent=self.labelFrame, text=self.browse_dict['choose MIDI file'])
        self.choose_midi_file_button.clicked.connect(self.fileDialog)
        self.choose_midi_file_button.move(115, 100)
        self.choose_midi_file_button.show()

    def redo(self):
        self.quit_normal_button.deleteLater()
        self.cancel_button.deleteLater()
        self.choose_track_ind_text.deleteLater()
        self.choose_track_ind.deleteLater()
        self.check_bpm_text.deleteLater()
        self.check_bpm.deleteLater()
        self.main_melody.deleteLater()
        self.merge_all_tracks.deleteLater()
        self.filename_label.deleteLater()
        self.make_button()

    def go_back(self):
        self.parent.action = 1
        self.close()

    def quit_normal(self):
        self.msg_label.setText('')
        self.parent.set_bpm = self.check_bpm.text()
        self.parent.off_melody = self.main_melody.isChecked()
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
            if piano_config.get_off_drums:
                while 9 in all_tracks.channels:
                    del all_tracks[all_tracks.channels.index(9)]
            if not self.parent.if_merge:
                if self.parent.track_ind_get is not None:
                    all_tracks = [
                        (current_bpm,
                         all_tracks.tracks[self.parent.track_ind_get],
                         all_tracks.start_times[self.parent.track_ind_get])
                    ]
                else:
                    all_tracks = [(current_bpm, all_tracks.tracks[0],
                                   all_tracks.start_times[0])]
                all_tracks[0][1].reset_track(0)
            else:
                all_tracks = [(current_bpm, all_tracks.tracks[i],
                               all_tracks.start_times[i])
                              for i in range(len(all_tracks.tracks))]

            pitch_bends = mp.concat(
                [i[1].split(mp.pitch_bend, get_time=True) for i in all_tracks])
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
                            while (colors == (255, 255, 255)) or (current_color
                                                                  in colors):
                                current_color = tuple(
                                    [random.randint(0, 255) for j in range(3)])
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
                    all_track_notes &= (current_track,
                                        current[2] - first_track_start_time)
            all_track_notes += pitch_bends
            if self.parent.set_bpm != '':
                tempo = float(self.parent.set_bpm)
            first_track_start_time += all_track_notes.start_time
            self.parent.read_result = tempo, all_track_notes, first_track_start_time, actual_start_time

        except Exception as e:
            print(str(e))
            self.parent.read_result = 'error'

        if self.parent.read_result != 'error':
            self.parent.sheetlen = len(self.parent.read_result[1])
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
            self.quit_normal_button.resize(80, 30)
            self.quit_normal_button.move(155, 100)
            self.cancel_button = QtWidgets.QPushButton(
                parent=self.labelFrame, text=self.browse_dict['cancel'])
            self.cancel_button.clicked.connect(self.redo)
            self.cancel_button.resize(80, 30)
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
            self.choose_track_ind_text.setFont(QtGui.QFont('Consolas', 10))
            self.choose_track_ind_text.move(100, 182)
            self.choose_track_ind_text.show()
            self.choose_track_ind = QtWidgets.QLineEdit(parent=self.labelFrame)
            self.choose_track_ind.setMaximumWidth(50)
            self.choose_track_ind.move(230, 180)
            self.choose_track_ind.show()
            self.check_bpm_text = QtWidgets.QLabel(parent=self.labelFrame,
                                                   text='BPM')
            self.check_bpm_text.move(155, 215)
            self.check_bpm_text.show()
            self.check_bpm = QtWidgets.QLineEdit(parent=self.labelFrame)
            self.check_bpm.setMaximumWidth(100)
            self.check_bpm.move(230, 215)
            self.check_bpm.show()
            self.main_melody = QtWidgets.QCheckBox(
                parent=self.labelFrame, text=self.browse_dict['melody'])
            self.main_melody.move(100, 250)
            self.main_melody.setFont(QtGui.QFont('Consolas', 10))
            self.main_melody.show()
            self.merge_all_tracks = QtWidgets.QCheckBox(
                parent=self.labelFrame, text=self.browse_dict['merge'])
            self.merge_all_tracks.setFont(QtGui.QFont('Consolas', 10))
            self.merge_all_tracks.move(250, 65)
            self.merge_all_tracks.setChecked(True)
            self.merge_all_tracks.show()


class setup:

    def __init__(self, browse_dict, file_name=None):
        importlib.reload(piano_config)
        self.file_path = None
        self.action = 0
        self.track_ind_get = None
        self.read_result = None
        self.sheetlen = None
        self.set_bpm = None
        self.off_melody = 0
        self.if_merge = True
        app = QtWidgets.QApplication(sys.argv)
        self.current_browse_window = browse_window(self,
                                                   browse_dict,
                                                   file_name=file_name)
        app.exec()
