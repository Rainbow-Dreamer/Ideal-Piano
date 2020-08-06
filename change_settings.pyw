from tkinter import *
from tkinter import ttk
from tkinter import filedialog
with open('config.py', encoding='utf-8') as f:
    exec(f.read())


def change(var, new, is_str=True):
    text = open('config.py').read()
    text_ls = list(text)
    var_len = len(var) + 1
    var_ind = text.index('\n' + var) + var_len
    next_line = text[var_ind:].index('\n')
    if is_str:
        text_ls[var_ind:var_ind + next_line] = f" = '{new}'"
    else:
        text_ls[var_ind:var_ind + next_line] = f" = {new}"
    with open('config.py', 'w') as f:
        f.write(''.join(text_ls))


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Settings")
        self.minsize(200, 300)
        self.wm_iconbitmap('piano.ico')

        self.value_dict = {}
        self.set_value('global volume', 'global_volume', False, 5)
        self.set_value('delay time', 'delay_time', False, 5)
        self.set_value('sound path', 'sound_path', width=30)
        self.set_value('bpm', 'bpm', False, 5)
        self.save = ttk.Button(self, text="save", command=self.save_current)
        self.save.grid()
        self.saved_text = ttk.Label(text='saved')
        self.change_sound_path_button = ttk.Button(
            self, text='change', command=self.change_sound_path)
        self.change_sound_path_button.place(x=450, y=170)

    def change_sound_path(self):
        file_path = filedialog.askdirectory(initialdir='.',
                                            title="choose sound path")
        sound_path_entry = self.value_dict['sound_path'][0]
        sound_path_entry.delete(0, END)
        sound_path_entry.insert(END, file_path + '/')

    def set_value(self,
                  value_name,
                  real_value,
                  is_str=True,
                  width=5,
                  borderwidth=10):
        value_label = ttk.LabelFrame(self,
                                     text=value_name,
                                     borderwidth=borderwidth)
        value_label.grid(padx=200, pady=5)
        value_entry = ttk.Entry(value_label, width=width)
        before_value = str(eval(real_value))
        if before_value == 'None':
            before_value = ''
        elif before_value == '':
            before_value = "''"
        value_entry.insert(0, before_value)
        value_entry.grid()
        self.value_dict[real_value] = [value_entry, before_value, is_str]

    def show_saved(self):
        self.saved_text.grid()
        self.after(1000, self.saved_text.grid_forget)

    def save_current(self):
        changed = False
        for each in self.value_dict:
            current_value = self.value_dict[each]
            current = current_value[0].get()
            if current != current_value[1]:
                if current == '':
                    current = 'None'
                change(each, current, current_value[2])
                self.value_dict[each][1] = current
                changed = True
        if changed:
            self.show_saved()


root = Root()
root.mainloop()
