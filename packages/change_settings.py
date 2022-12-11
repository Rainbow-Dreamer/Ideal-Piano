from ast import literal_eval
import sys, os
from PyQt5 import QtGui, QtWidgets, QtCore
import json
from copy import deepcopy as copy


def set_font(font, dpi):
    if dpi != 96.0:
        font.setPointSize(font.pointSize() * (96.0 / dpi))
    return font


def save_json(config, config_path, whole_config=None):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config if not whole_config else whole_config,
                  f,
                  indent=4,
                  separators=(',', ': '),
                  ensure_ascii=False)


def change_parameter(var, new, config_path, whole_config=None):
    if os.path.exists(config_path):
        with open(config_path, encoding='utf-8') as f:
            current_config = json.load(f)
        if var in current_config:
            current_config[var] = new
            save_json(current_config, config_path, whole_config)


class json_module:

    def __init__(self, file, text=None):
        if text is None:
            with open(file, encoding='utf-8') as f:
                text = json.load(f)
        self.json = text
        for i, j in self.json.items():
            setattr(self, i, j)


class Dialog(QtWidgets.QMainWindow):

    def __init__(self, caption, directory, filter, mode=0):
        super().__init__()
        if mode == 0:
            self.filename = QtWidgets.QFileDialog.getOpenFileName(
                self, caption=caption, directory=directory, filter=filter)
        elif mode == 1:
            self.directory = QtWidgets.QFileDialog.getExistingDirectory(
                self, caption=caption, directory=directory)
        elif mode == 2:
            self.filename = QtWidgets.QFileDialog.getSaveFileName(
                self, caption=caption, directory=directory, filter=filter)


class config_window(QtWidgets.QMainWindow):

    def __init__(self, dpi=None, config_path=''):
        super().__init__()
        if sys.platform == 'win32':
            self.setWindowIcon(QtGui.QIcon('resources/piano.ico'))
        elif sys.platform == 'linux':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.png'))
        elif sys.platform == 'darwin':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.icns'))
        self.config_path = config_path
        self.whole_config = None
        self.current_config = self.whole_config
        self.current_path = []
        self.dpi = dpi
        self.sort_mode = 0
        self.search_inds = 0
        self.search_inds_list = []

        self.setWindowTitle("Settings")
        self.setMinimumSize(800, 600)
        self.setFont(set_font(QtGui.QFont('Consolas', 10), self.dpi))

        self.choose_config_file_button = QtWidgets.QPushButton(
            self, text='choose json file')
        self.choose_config_file_button.clicked.connect(self.choose_json_file)
        self.choose_config_file_button.setFixedWidth(150)
        self.choose_config_file_button.move(0, 10)

        self.choose_config_options = QtWidgets.QListWidget(self)
        self.choose_config_options.clicked.connect(
            self.show_current_config_options)
        self.choose_config_options.resize(250, 200)
        self.choose_config_options.move(0, 50)
        self.config_name = QtWidgets.QLabel(self, text='')
        self.config_name.setFixedWidth(300)
        self.config_name.move(365, 20)
        self.config_contents = QtWidgets.QPlainTextEdit(self)
        self.config_contents.setFont(
            set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.config_contents.textChanged.connect(self.config_change)
        self.config_contents.resize(400, 400)
        self.config_contents.move(365, 50)

        self.choose_filename_button = QtWidgets.QPushButton(
            self, text='choose filename')
        self.choose_filename_button.clicked.connect(self.choose_filename)
        self.choose_filename_button.setFixedWidth(150)
        self.choose_filename_button.move(0, 270)
        self.choose_directory_button = QtWidgets.QPushButton(
            self, text='choose directory')
        self.choose_directory_button.clicked.connect(self.choose_directory)
        self.choose_directory_button.setFixedWidth(150)
        self.choose_directory_button.move(0, 320)

        self.save = QtWidgets.QPushButton(self, text="save")
        self.save.clicked.connect(self.save_current)
        self.save.move(0, 400)
        self.save_shortcut = QtWidgets.QShortcut('Ctrl+S', self)
        self.save_shortcut.activated.connect(self.save_current)
        self.saved_text = QtWidgets.QLabel(self, text='saved')
        self.saved_text.move(50, 530)
        self.saved_text.hide()

        self.search_text = QtWidgets.QLabel(self,
                                            text='search for config options')
        self.search_text.setFixedWidth(200)
        self.search_text.move(0, 450)
        self.search_entry = QtWidgets.QLineEdit(self)
        self.search_entry.setFixedWidth(200)
        self.search_entry.textChanged.connect(self.search)
        self.search_entry.move(0, 480)

        self.up_button = QtWidgets.QPushButton(self, text='Previous')
        self.up_button.clicked.connect(lambda: self.change_search_inds(-1))
        self.down_button = QtWidgets.QPushButton(self, text='Next')
        self.down_button.clicked.connect(lambda: self.change_search_inds(1))
        self.up_button.move(220, 480)
        self.down_button.move(350, 480)

        self.export_button = QtWidgets.QPushButton(self, text='Export')
        self.export_button.clicked.connect(self.export_json)
        self.export_button.move(480, 480)

        self.choose_bool1 = QtWidgets.QPushButton(self, text='True')
        self.choose_bool1.clicked.connect(lambda: self.insert_bool('True'))
        self.choose_bool1.setFixedWidth(80)
        self.choose_bool2 = QtWidgets.QPushButton(self, text='False')
        self.choose_bool2.clicked.connect(lambda: self.insert_bool('False'))
        self.choose_bool2.setFixedWidth(80)
        self.choose_bool1.move(165, 320)
        self.choose_bool2.move(260, 320)

        self.back_button = QtWidgets.QPushButton(self, text='Back')
        self.back_button.clicked.connect(self.back_func)
        self.back_button.setFixedWidth(80)
        self.forward_button = QtWidgets.QPushButton(self, text='Forward')
        self.forward_button.clicked.connect(self.forward_func)
        self.forward_button.setFixedWidth(80)
        self.back_button.move(165, 270)
        self.forward_button.move(260, 270)

        self.change_sort_button = QtWidgets.QPushButton(
            self, text="sort in alphabetical order")
        self.change_sort_button.clicked.connect(self.change_sort)
        self.change_sort_button.setFixedWidth(220)
        self.change_sort_button.setFont(
            set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.change_sort_button.move(120, 400)

        self.edit_list_button = QtWidgets.QPushButton(self,
                                                      text='Edit json in list')
        self.edit_list_button.setFixedWidth(150)
        self.edit_list_button.clicked.connect(self.edit_json_in_list)
        self.edit_list_button.move(180, 10)

        if self.config_path:
            self.load_current_file()

        self.show()

    def load_current_file(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as f:
                self.whole_config = json.load(f)
            self.current_config = self.whole_config
            self.current_config_original = copy(self.whole_config)
            self.current_config_keys = list(self.whole_config.keys())
            self.current_config_alpha_keys = list(
                sorted(self.current_config_keys, key=lambda s: s.lower()))
            self.options_num = len(self.whole_config)
            self.config_contents.clear()
            self.set_sort()

    def reload_current_file(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as f:
                self.whole_config = json.load(f)

    def load_current_config(self):
        self.current_config_original = copy(self.current_config)
        self.current_config_keys = list(self.current_config.keys())
        self.current_config_alpha_keys = list(
            sorted(self.current_config_keys, key=lambda s: s.lower()))
        self.options_num = len(self.current_config)
        self.config_contents.clear()
        self.set_sort()

    def choose_json_file(self):
        last_path = ''
        if os.path.exists('last_path.txt'):
            with open('last_path.txt', encoding='utf-8') as f:
                last_path = f.read()
        filename = Dialog(
            caption='choose json file',
            directory=last_path,
            filter='json files (*.json);all files (*)').filename[0]
        if filename:
            current_path = os.path.dirname(filename)
            if current_path != last_path:
                with open('last_path.txt', 'w', encoding='utf-8') as f:
                    f.write(current_path)
            self.config_path = filename
            try:
                self.load_current_file()
            except:
                pass

    def export_json(self):
        if self.whole_config:
            last_path = ''
            if os.path.exists('last_path.txt'):
                with open('last_path.txt', encoding='utf-8') as f:
                    last_path = f.read()
            filename = Dialog(caption='choose save path',
                              directory=self.config_path,
                              filter='all files (*)',
                              mode=2).filename[0]
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.whole_config,
                              f,
                              indent=4,
                              separators=(',', ': '),
                              ensure_ascii=False)

    def forward_func(self, args, ind=None):
        if self.current_config:
            current_selected_items = self.choose_config_options.selectedItems()
            if current_selected_items:
                current_config = current_selected_items[0].text()
                self.config_name.setText(current_config)
                current_config_value = self.current_config[current_config]
                if current_config_value:
                    if isinstance(current_config_value, dict):
                        self.current_path.append(current_config)
                        self.current_config = current_config_value
                        self.load_current_config()
                    elif isinstance(current_config_value, list):
                        if type(ind) != int:
                            ind = 0
                        if isinstance(current_config_value[ind], dict):
                            self.current_path.append(current_config)
                            self.current_path.append(ind)
                            self.current_config = current_config_value[ind]
                            self.load_current_config()

    def back_func(self):
        if self.current_config:
            if self.current_path:
                current_key = self.current_path.pop()
                if not self.current_path:
                    current = self.whole_config
                else:
                    current = self.whole_config[self.current_path[0]]
                    for each in self.current_path[1:]:
                        current = current[each]
                    while isinstance(current, list):
                        current_key = self.current_path.pop()
                        if not self.current_path:
                            current = self.whole_config
                        else:
                            current = self.whole_config[self.current_path[0]]
                            for each in self.current_path[1:]:
                                current = current[each]
                self.current_config = current
                self.load_current_config()
                if self.sort_mode == 0:
                    current_ind = self.current_config_alpha_keys.index(
                        current_key)
                elif self.sort_mode == 1:
                    current_ind = self.current_config_keys.index(current_key)
                self.choose_config_options.setCurrentRow(current_ind)
                self.show_current_config_options()

    def load_current_path(self):
        if self.whole_config:
            if not self.current_path:
                current = self.whole_config
            else:
                current = self.whole_config[self.current_path[0]]
                for each in self.current_path[1:]:
                    current = current[each]
            self.current_config = current

    def edit_json_in_list(self):
        if self.current_config:
            current_selected_items = self.choose_config_options.selectedItems()
            if current_selected_items:
                current_config = current_selected_items[0].text()
                self.config_name.setText(current_config)
                current_config_value = self.current_config[current_config]
                if isinstance(current_config_value, list):
                    current_json = [
                        i for i in current_config_value if isinstance(i, dict)
                    ]
                    if current_json:
                        current_pos = QtGui.QCursor.pos()
                        current_menu = QtWidgets.QMenu(self)
                        for i, each in enumerate(current_json):
                            current = current_menu.addAction(f'json {i+1}')
                            current.triggered.connect(
                                lambda args, i=i: self.forward_func(args, i))
                        current_menu.exec(current_pos)

    def change_sort(self):
        if self.current_config:
            if self.sort_mode == 0:
                self.sort_mode = 1
                self.change_sort_button.setText('sort in order of appearance')
                self.choose_config_options.clear()
                for k, each in enumerate(self.current_config_keys):
                    self.choose_config_options.insertItem(k, each)
            else:
                self.sort_mode = 0
                self.change_sort_button.setText('sort in alphabetical order')
                self.choose_config_options.clear()
                for k, each in enumerate(self.current_config_alpha_keys):
                    self.choose_config_options.insertItem(k, each)
            self.search()

    def set_sort(self):
        if self.current_config:
            if self.sort_mode == 1:
                self.change_sort_button.setText('sort in order of appearance')
                self.choose_config_options.clear()
                for k, each in enumerate(self.current_config_keys):
                    self.choose_config_options.insertItem(k, each)
            else:
                self.change_sort_button.setText('sort in alphabetical order')
                self.choose_config_options.clear()
                for k, each in enumerate(self.current_config_alpha_keys):
                    self.choose_config_options.insertItem(k, each)

    def insert_bool(self, content):
        if self.current_config:
            self.config_contents.setPlainText(content)
            self.config_change()

    def config_change(self):
        if self.current_config:
            try:
                current = literal_eval(self.config_contents.toPlainText())
                current_config = self.choose_config_options.selectedItems(
                )[0].text()
                self.current_config[current_config] = current
            except:
                pass

    def change_search_inds(self, num):
        self.search_inds += num
        if self.search_inds < 0:
            self.search_inds = 0
        if self.search_inds_list:
            search_num = len(self.search_inds_list)
            if self.search_inds >= search_num:
                self.search_inds = search_num - 1
            first = self.search_inds_list[self.search_inds]
            self.choose_config_options.setCurrentRow(first)
            self.show_current_config_options()

    def search(self):
        if self.current_config:
            current = self.search_entry.text()
            if not current:
                self.choose_config_options.clearSelection()
                return
            current_keys = self.current_config_keys if self.sort_mode == 1 else self.current_config_alpha_keys
            self.search_inds_list = [
                i for i in range(self.options_num)
                if current.lower() in current_keys[i].lower()
            ]
            if self.search_inds_list:
                self.search_inds = 0
                first = self.search_inds_list[self.search_inds]
                self.choose_config_options.setCurrentRow(first)
                self.show_current_config_options()
            else:
                self.choose_config_options.clearSelection()

    def show_current_config_options(self):
        if self.current_config:
            current_config = self.choose_config_options.selectedItems(
            )[0].text()
            self.config_name.setText(current_config)
            current_config_value = self.current_config[current_config]
            if type(current_config_value) == str:
                current_config_value = f"'{current_config_value}'"
            else:
                current_config_value = str(current_config_value)
            self.config_contents.setPlainText(current_config_value)

    def choose_filename(self):
        if self.current_config:
            last_path = ''
            if os.path.exists('last_path.txt'):
                with open('last_path.txt', encoding='utf-8') as f:
                    last_path = f.read()
            filename = Dialog(caption='choose filename',
                              directory=last_path,
                              filter='all files (*)').filename[0]
            if filename:
                current_path = os.path.dirname(filename)
                if current_path != last_path:
                    with open('last_path.txt', 'w', encoding='utf-8') as f:
                        f.write(current_path)
                self.config_contents.setPlainText(f"'{filename}'")
                self.config_change()

    def choose_directory(self):
        if self.current_config:
            last_path = ''
            if os.path.exists('last_path.txt'):
                with open('last_path.txt', encoding='utf-8') as f:
                    last_path = f.read()
            directory = Dialog(caption='choose directory',
                               directory=last_path,
                               filter='all files (*)',
                               mode=1).directory
            if directory:
                current_path = directory
                if current_path != last_path:
                    with open('last_path.txt', 'w', encoding='utf-8') as f:
                        f.write(current_path)
                self.config_contents.setPlainText(f"'{directory}'")
                self.config_change()

    def show_saved(self):
        self.saved_text.show()
        QtCore.QTimer.singleShot(1000, self.saved_text.hide)

    def save_current(self):
        if self.current_config:
            changed = False
            for each, current_value in self.current_config.items():
                before_value = self.current_config_original[each]
                if current_value != before_value:
                    save_json(self.current_config, self.config_path,
                              self.whole_config)
                    self.current_config_original[each] = current_value
                    changed = True
            if changed:
                self.show_saved()
                if self.current_path:
                    self.reload_current_file()
                    self.load_current_path()
