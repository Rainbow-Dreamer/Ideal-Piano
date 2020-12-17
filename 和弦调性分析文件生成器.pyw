from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("和弦调性分析文件生成器")
        self.minsize(900, 600)
        self.text = ''
        self.preview = Text(self,
                            width=40,
                            height=20,
                            undo=True,
                            maxundo=-1,
                            autoseparators=False)
        self.preview.configure(font=("Consolas", 12))
        self.preview.place(x=510, y=0)
        self.preview.bind("<Control-z>", self.undo_func)
        self.preview.bind("<Control-y>", self.redo_func)
        self.preview_label = ttk.Label(self, text='预览')
        self.preview_label.place(x=510, y=410)
        self.enter_key = ttk.Button(self,
                                    text='输入调性',
                                    command=self.enter_key_func)
        self.enter_key.place(x=0, y=100)
        self.enter_key_entry = ttk.Entry(self, width=20)
        self.enter_key_entry.place(x=100, y=100)
        self.msg = ttk.Label(self, text='')
        self.msg.place(x=500, y=450)
        self.save = ttk.Button(self, text='保存预览', command=self.save_current)
        self.save.place(x=0, y=30)
        self.output_as_file = ttk.Button(self, text='导出', command=self.output)
        self.output_as_file.place(x=100, y=30)
        self.input_as_file = ttk.Button(self,
                                        text='导入',
                                        command=self.input_file)
        self.input_as_file.place(x=200, y=30)
        self.enter_new_bar = ttk.Button(self,
                                        text='输入小节',
                                        command=self.enter_bar)
        self.enter_new_bar.place(x=0, y=150)
        self.enter_new_bar_entry = ttk.Entry(self, width=20)
        self.enter_new_bar_entry.place(x=100, y=150)
        self.bar_type_value = IntVar()
        self.bar_type1 = Radiobutton(self,
                                     text='相对小节数',
                                     value=1,
                                     variable=self.bar_type_value)
        self.bar_type2 = Radiobutton(self,
                                     text='绝对小节数',
                                     value=2,
                                     variable=self.bar_type_value)
        self.bar_type_value.set(1)
        self.bar_type1.place(x=0, y=200)
        self.bar_type2.place(x=100, y=200)
        self.enter_newline = ttk.Button(self,
                                        text='输入空行',
                                        command=self.enter_newline_func)
        self.enter_newline.place(x=0, y=250)
        self.enter_chord = ttk.Button(self,
                                      text='输入和弦名称',
                                      command=self.enter_chord_name)
        self.enter_chord.place(x=0, y=300)
        self.enter_chord_entry = ttk.Entry(self, width=20)
        self.enter_chord_entry.place(x=100, y=300)
        self.current_bar_chords = []
        self.enter_chord_degree = ttk.Button(
            self, text='输入和弦级数', command=self.enter_chord_degree_func)
        self.enter_chord_degree.place(x=0, y=350)
        self.enter_chord_degree_entry = ttk.Entry(self, width=20)
        self.enter_chord_degree_entry.place(x=100, y=350)
        self.chord_inds = []
        self.current_bar_chords_degree = []
        self.degree_inds = []
        self.add_comments = ttk.Button(self,
                                       text='为当前小节加入说明',
                                       command=self.bar_add_comments)
        self.add_comments.place(x=300, y=50)
        self.add_comments_entry = Text(self, width=25, height=15)
        self.add_comments_entry.place(x=300, y=100)
        self.current_play = IntVar()
        self.current_play_button = Checkbutton(self,
                                               text='显示此时正在演奏这个和弦',
                                               variable=self.current_play,
                                               onvalue=1,
                                               offvalue=0)
        self.current_play_button.place(x=0, y=400)
        self.current_play_set = False
        self.current_play_num = 0
        self.undo_button = ttk.Button(self, text='撤销', command=self.undo_func)
        self.undo_button.place(x=300, y=350)
        self.redo_button = ttk.Button(self, text='恢复', command=self.redo_func)
        self.redo_button.place(x=300, y=450)
        self.clear_all = ttk.Button(self,
                                    text='清空',
                                    command=self.clear_preview)
        self.clear_all.place(x=400, y=350)
        self.last_line = ttk.Button(self,
                                    text='收尾',
                                    command=self.add_last_line)
        self.last_line.place(x=300, y=400)
        self.undo_chord = ttk.Button(self,
                                     text='撤销和弦',
                                     command=self.undo_last_chord)
        self.undo_chord.place(x=400, y=400)
        self.interval = 1
        self.interval_button = ttk.Button(self,
                                          text='改变小节线间隔',
                                          command=self.change_interval)
        self.interval_button.place(x=0, y=450)
        self.interval_entry = ttk.Entry(self, width=20)
        self.interval_entry.place(x=100, y=450)
        self.interval_entry.insert(END, self.interval)
        self.enter_grammar = ttk.Button(self,
                                        text='输入特殊批处理语句',
                                        command=self.grammar_translate)
        self.enter_grammar.place(x=0, y=500)
        self.enter_grammar_entry = ttk.Entry(self, width=80)
        self.enter_grammar_entry.place(x=140, y=500)
        self.enter_grammar_entry.configure(font=('Consolas', 12))

    def grammar_translate(self):
        current = self.enter_grammar_entry.get()
        if current[:2] == 'k.':
            current_key = current[2:]
            self.text += f'key: {current_key}\n\n'
            self.refresh_preview()
            self.msg.configure(text='已成功解析语句')
            return
        parts = current.split('$')
        length = len(parts)
        if length == 2:
            bar_chords, chord_degrees = parts
        elif length == 3:
            bar_chords, chord_degrees, comments = parts
        else:
            self.msg.configure(text='输入的特殊批处理语句不符合语法')
            return
        bar_chords_split = bar_chords.split(';')
        bar_num = bar_chords_split[0]
        current_chords = bar_chords_split[1:]
        current_play = False
        current_play_num = 0
        for i in range(len(current_chords)):
            each = current_chords[i]
            if each[0] == '!':
                current_play = True
                current_play_num = i
                current_chords[i] = each[1:]
        chord_degrees = chord_degrees.split(';')

        if self.text:
            if self.text[(-2 * self.interval -
                          1):] == f'{" "*self.interval}|{" "*self.interval}':
                self.text = self.text[:(-2 * self.interval - 1)] + '\n\n'
            elif self.text[-1] != '\n':
                self.text += '\n\n'
        self.text += f'{bar_num}\n'
        self.current_bar_chords.clear()
        self.current_bar_chords_degree.clear()
        self.degree_inds.clear()
        self.chord_inds.clear()
        self.current_play_set = False
        self.current_play_num = 0

        current_chord_num = len(current_chords)
        chord_degrees_num = len(chord_degrees)
        for k in range(current_chord_num):
            chord_name = current_chords[k]
            if current_play and k == current_play_num:
                chord_name = '→ ' + chord_name
                self.current_play.set(0)
            self.text += f'{chord_name}{" "*self.interval}|{" "*self.interval}'

        if current_chord_num == 0:
            self.msg.configure(text='当前的小节还没有任何和弦')
            return
        for current_ind in range(chord_degrees_num):
            chord_degree = chord_degrees[current_ind]
            if current_ind == 0:
                self.recent_line = self.text[self.text.rfind('\n') + 1:]
                self.text = self.text[:(-2 * self.interval - 1)] + '\n'
                inds = 0
                if current_play and current_play_num == 0:
                    inds += 2
                self.text += ' ' * inds + chord_degree
                self.chord_inds = [
                    j + self.interval + 1 for j in range(len(self.recent_line))
                    if self.recent_line[j] == '|'
                ]
                if current_play and current_play_num != 0:
                    self.chord_inds[current_play_num - 1] += 2
            else:
                inds = self.chord_inds[current_ind - 1]
                last_degree = chord_degrees[current_ind - 1]
                last_degree_len = len(last_degree)
                last_chord = current_chords[current_ind - 1]
                self.text += ' ' * (inds - self.degree_inds[-1] -
                                    last_degree_len) + chord_degree
            self.degree_inds.append(inds)

        if length == 3:
            comments = comments.replace('\\n', '\n')
            self.text += f'\n{comments}'

        self.refresh_preview()
        self.msg.configure(text='已成功解析语句')

    def undo_last_chord(self):
        self.undo_func()
        self.preview.edit_separator()
        if self.chord_inds:
            del self.degree_inds[-1]
            del self.current_bar_chords_degree[-1]
            if not self.current_bar_chords_degree:
                self.chord_inds.clear()
        elif self.current_bar_chords:
            del self.current_bar_chords[-1]

    def input_file(self):
        filename = filedialog.askopenfilename(initialdir='.',
                                              title="打开文本",
                                              filetype=(("所有文件", "*.*"), ),
                                              defaultextension=".txt")
        if filename:
            with open(filename, encoding='utf-8-sig') as f:
                self.text = f.read()
                self.refresh_preview()
            self.msg.configure(text='导入文本文件成功')

    def change_interval(self):
        self.interval = int(self.interval_entry.get())

    def undo_func(self, e=None):
        try:
            self.preview.edit_undo()
            self.text = self.preview.get('1.0', 'end-1c')
        except:
            pass

    def redo_func(self, e=None):
        try:
            self.preview.edit_redo()
            self.text = self.preview.get('1.0', 'end-1c')
        except:
            pass

    def enter_key_func(self):
        current_key = self.enter_key_entry.get()
        if not current_key:
            self.msg.configure(text='当前并未输入任何调性')
        else:
            self.text += f'key: {current_key}\n\n'
            self.refresh_preview()
            self.msg.configure(text='已成功输入调性')

    def refresh_preview(self):
        self.preview.delete('1.0', END)
        self.preview.insert(END, self.text)
        self.preview.edit_separator()
        self.preview.see(INSERT)

    def clear_preview(self):
        self.preview.delete('1.0', END)
        self.text = self.preview.get('1.0', 'end-1c')
        self.preview.edit_separator()

    def save_current(self):
        self.text = self.preview.get('1.0', 'end-1c')
        self.msg.configure(text='保存当前预览成功')

    def output(self):
        filename = filedialog.asksaveasfilename(initialdir='.',
                                                title="保存输入文本",
                                                filetype=(("所有文件", "*.*"), ),
                                                defaultextension=".txt")
        if filename:
            with open(filename, 'w', encoding='utf-8-sig') as f:
                f.write(self.text)
            self.msg.configure(text='导出当前预览成功')

    def enter_bar(self):
        bar = self.enter_new_bar_entry.get()
        if not bar:
            self.msg.configure(text='当前并未输入任何小节')
        else:
            if self.text:
                if self.text[(
                        -2 * self.interval -
                        1):] == f'{" "*self.interval}|{" "*self.interval}':
                    self.text = self.text[:(-2 * self.interval - 1)] + '\n\n'
                elif self.text[-1] != '\n':
                    self.text += '\n\n'
            bar_type = self.bar_type_value.get()
            if bar_type == 1:
                self.text += f'+{bar}\n'
            elif bar_type == 2:
                self.text += f'{bar}\n'
            self.refresh_preview()
            self.msg.configure(text='已成功输入小节')
            self.current_bar_chords.clear()
            self.current_bar_chords_degree.clear()
            self.degree_inds.clear()
            self.chord_inds.clear()
            self.current_play_set = False
            self.current_play_num = 0

    def enter_newline_func(self):
        self.text += '\n'
        self.refresh_preview()
        self.msg.configure(text='已成功输入空行')

    def enter_chord_name(self):
        chord_name = self.enter_chord_entry.get()
        if not chord_name:
            self.msg.configure(text='当前并未输入任何和弦')
        else:
            current_play = self.current_play.get()
            if current_play == 1:
                if not self.current_play_set:
                    chord_name = '→ ' + chord_name
                    self.current_play_num = len(self.current_bar_chords)
                    self.current_play_set = True
                else:
                    self.msg.configure(text='这个小节已经有正在演奏的和弦了')
                self.current_play.set(0)
            self.text += f'{chord_name}{" "*self.interval}|{" "*self.interval}'
            self.refresh_preview()
            self.current_bar_chords.append(chord_name)

    def enter_chord_degree_func(self):
        chord_degree = self.enter_chord_degree_entry.get()
        if not chord_degree:
            self.msg.configure(text='当前并未输入任何和弦级数')
        else:
            current_chord_num = len(self.current_bar_chords)
            if current_chord_num == 0:
                self.msg.configure(text='当前的小节还没有任何和弦')
                return
            current_ind = len(self.current_bar_chords_degree)
            if current_ind >= current_chord_num:
                self.msg.configure(text='当前小节的和弦已经全配上级数了，请开新的小节')
            else:
                if current_ind == 0:
                    self.recent_line = self.text[self.text.rfind('\n') + 1:]
                    self.text = self.text[:(-2 * self.interval - 1)] + '\n'
                    inds = 0
                    if self.current_play_set and self.current_play_num == 0:
                        inds += 2
                    self.text += ' ' * inds + chord_degree
                    self.chord_inds = [
                        j + self.interval + 1
                        for j in range(len(self.recent_line))
                        if self.recent_line[j] == '|'
                    ]
                    if self.current_play_set and self.current_play_num != 0:
                        self.chord_inds[self.current_play_num - 1] += 2
                else:
                    inds = self.chord_inds[current_ind - 1]
                    last_degree = self.current_bar_chords_degree[-1]
                    last_degree_len = len(last_degree)
                    last_chord = self.current_bar_chords[current_ind - 1]
                    self.text += ' ' * (inds - self.degree_inds[-1] -
                                        last_degree_len) + chord_degree
                self.degree_inds.append(inds)
                self.refresh_preview()
                self.current_bar_chords_degree.append(chord_degree)

    def bar_add_comments(self):
        comments = self.add_comments_entry.get('1.0', 'end-1c')
        if not comments:
            self.msg.configure(text='当前并未输入任何说明')
            return
        self.text += f'\n{comments}'
        self.refresh_preview()
        self.msg.configure(text='已成功为当前小节加入说明')

    def add_last_line(self):
        if self.text[(-2 * self.interval -
                      1):] == f'{" "*self.interval}|{" "*self.interval}':
            self.text = self.text[:(-2 * self.interval - 1)]
        self.text += '\n\n'
        self.refresh_preview()


root = Root()
root.mainloop()