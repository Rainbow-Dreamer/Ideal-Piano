from ast import literal_eval
import sys, os
from PyQt5 import QtGui, QtWidgets, QtCore


def set_font(font, dpi):
    if dpi != 96.0:
        font.setPointSize(font.pointSize() * (96.0 / dpi))
    return font


def get_all_config_options(text):
    result = []
    N = len(text)
    for i in range(N):
        current = text[i]
        if current == '\n':
            if i + 1 < N:
                next_character = text[i + 1]
                if next_character.isalpha():
                    inds = text[i + 1:].index('=') - 1
                    current_config_options = text[i + 1:i + 1 + inds]
                    result.append(current_config_options)
    return result


def change(var, new, is_str=True):
    text = open(config_path, encoding='utf-8').read()
    text_ls = list(text)
    var_len = len(var) + 1
    var_ind = text.index('\n' + var + ' ') + var_len
    current_var_ind = all_config_options_ind[var]
    if current_var_ind < len(all_config_options) - 1:
        next_var = config_original[current_var_ind + 1]
        next_var_ind = text.index('\n' + next_var + ' ')
        next_comments_ind = text[var_ind:].find('\n\n')
        if next_comments_ind != -1:
            next_comments_ind += var_ind
            if next_comments_ind < next_var_ind:
                next_var_ind = next_comments_ind
    else:
        next_var_ind = -1
    if is_str:
        text_ls[var_ind:next_var_ind] = f" = '{new}'"
    else:
        text_ls[var_ind:next_var_ind] = f" = {new}"
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(''.join(text_ls))


class Dialog(QtWidgets.QMainWindow):

    def __init__(self, caption, directory, filter, mode=0):
        super().__init__()
        if mode == 0:
            self.filename = QtWidgets.QFileDialog.getOpenFileName(
                self, caption=caption, directory=directory, filter=filter)
        elif mode == 1:
            self.directory = QtWidgets.QFileDialog.getExistingDirectory(
                self, caption=caption, directory=directory)


class config_window(QtWidgets.QMainWindow):

    def __init__(self, dpi=None):
        with open(config_path, encoding='utf-8') as f:
            text = f.read()
            exec(text, globals(), globals())
        super().__init__()
        self.dpi = dpi
        self.setWindowTitle("Settings")
        self.setMinimumSize(800, 600)
        self.setFont(set_font(QtGui.QFont('Consolas', 10), self.dpi))
        if sys.platform == 'win32':
            self.setWindowIcon(QtGui.QIcon('resources/piano.ico'))
        elif sys.platform == 'linux':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.png'))
        elif sys.platform == 'darwin':
            self.setWindowIcon(QtGui.QIcon('resources/piano_icon.icns'))
        self.choose_config_options = QtWidgets.QListWidget(self)
        self.choose_config_options.clicked.connect(
            self.show_current_config_options)
        global all_config_options
        all_config_options = get_all_config_options(text)
        self.options_num = len(all_config_options)
        global all_config_options_ind
        all_config_options_ind = {
            all_config_options[i]: i
            for i in range(self.options_num)
        }
        global config_original
        config_original = all_config_options.copy()
        all_config_options.sort(key=lambda s: s.lower())
        global alpha_config
        alpha_config = all_config_options.copy()
        for k, each in enumerate(all_config_options):
            self.choose_config_options.insertItem(k, each)
        self.choose_config_options.resize(220, 170)
        self.choose_config_options.move(0, 30)
        self.config_name = QtWidgets.QLabel(self, text='')
        self.config_name.setFixedWidth(300)
        self.config_name.move(300, 20)
        self.config_contents = QtWidgets.QPlainTextEdit(self)
        self.config_contents.setFont(
            set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.config_contents.textChanged.connect(self.config_change)
        self.config_contents.resize(400, 400)
        self.config_contents.move(350, 50)
        self.choose_filename_button = QtWidgets.QPushButton(
            self, text='choose filename')
        self.choose_filename_button.clicked.connect(self.choose_filename)
        self.choose_filename_button.setFixedWidth(150)
        self.choose_filename_button.move(0, 250)
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
        self.search_inds = 0
        self.up_button = QtWidgets.QPushButton(self, text='Previous')
        self.up_button.clicked.connect(lambda: self.change_search_inds(-1))
        self.down_button = QtWidgets.QPushButton(self, text='Next')
        self.down_button.clicked.connect(lambda: self.change_search_inds(1))
        self.up_button.move(220, 480)
        self.down_button.move(350, 480)
        self.search_inds_list = []
        self.value_dict = {i: str(eval(i)) for i in all_config_options}
        self.choose_bool1 = QtWidgets.QPushButton(self, text='True')
        self.choose_bool1.clicked.connect(lambda: self.insert_bool('True'))
        self.choose_bool1.setFixedWidth(80)
        self.choose_bool2 = QtWidgets.QPushButton(self, text='False')
        self.choose_bool2.clicked.connect(lambda: self.insert_bool('False'))
        self.choose_bool2.setFixedWidth(80)
        self.choose_bool1.move(160, 270)
        self.choose_bool2.move(260, 270)
        self.change_sort_button = QtWidgets.QPushButton(
            self, text="sort in alphabetical order")
        self.change_sort_button.clicked.connect(self.change_sort)
        self.change_sort_button.setFixedWidth(200)
        self.change_sort_button.setFont(
            set_font(QtGui.QFont('Consolas', 10), self.dpi))
        self.sort_mode = 0
        self.change_sort_button.move(140, 400)
        self.show()

    def change_sort(self):
        global all_config_options
        if self.sort_mode == 0:
            self.sort_mode = 1
            self.change_sort_button.setText('sort in order of appearance')
            all_config_options = config_original.copy()
            self.choose_config_options.clear()
            for k, each in enumerate(all_config_options):
                self.choose_config_options.insertItem(k, each)
        else:
            self.sort_mode = 0
            self.change_sort_button.setText('sort in alphabetical order')
            all_config_options = alpha_config.copy()
            self.choose_config_options.clear()
            for k, each in enumerate(all_config_options):
                self.choose_config_options.insertItem(k, each)
        self.search()

    def insert_bool(self, content):
        self.config_contents.setPlainText(content)
        self.config_change()

    def config_change(self):
        try:
            current = self.config_contents.toPlainText()
            current = literal_eval(current)
            if type(current) == str:
                current = f"'{current}'"
            current_config = self.choose_config_options.selectedItems(
            )[0].text()
            exec(f'{current_config} = {current}', globals())
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
        current = self.search_entry.text()
        if not current:
            return
        self.search_inds_list = [
            i for i in range(self.options_num)
            if current in all_config_options[i]
        ]
        if self.search_inds_list:
            self.search_inds = 0
            first = self.search_inds_list[self.search_inds]
            self.choose_config_options.setCurrentRow(first)
            self.show_current_config_options()
        else:
            self.choose_config_options.clearSelection()

    def show_current_config_options(self):
        current_config = self.choose_config_options.selectedItems()[0].text()
        if current_config:
            self.config_name.setText(current_config)
            current_config_value = eval(current_config)
            if type(current_config_value) == str:
                current_config_value = f"'{current_config_value}'"
            else:
                current_config_value = str(current_config_value)
            self.config_contents.setPlainText(current_config_value)

    def choose_filename(self):
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
        changed = False
        for each in all_config_options:
            current_value = eval(each)
            current_value_str = str(current_value)
            before_value = self.value_dict[each]
            if current_value_str != before_value:
                change(each, current_value_str, type(current_value) == str)
                self.value_dict[each] = current_value_str
                changed = True
        if changed:
            self.show_saved()


config_path = 'packages/piano_config.py'
