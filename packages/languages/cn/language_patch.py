from musicpy import *

globals().update(database.interval_dict)

# database

INTERVAL = {
    0: '纯一度',
    1: '小二度',
    2: '大二度',
    3: '小三度',
    4: '大三度',
    5: '纯四度',
    6: '减五度',
    7: '纯五度',
    8: '小六度',
    9: '大六度',
    10: '小七度',
    11: '大七度',
    12: '纯八度',
    13: '小九度',
    14: '大九度',
    15: '小三度 / 增九度',
    16: '大三度 / 大十度',
    17: '纯十一度',
    18: '增十一度',
    19: '纯十二度',
    20: '小十三度',
    21: '大十三度'
}

chordTypes = database.match({
    ('大三和弦', 'major', 'M', 'maj', 'majorthird'): (M3, P5),
    ('小三和弦', 'minor', 'm', 'minorthird', 'min', '-'): (m3, P5),
    ('大七和弦', 'maj7', 'M7', 'major7th', 'majorseventh'): (M3, P5, M7),
    ('小七和弦', 'm7', 'min7', 'minor7th', 'minorseventh', '-7'): (m3, P5, m7),
    ('属七和弦(大小七和弦)', '7', 'seven', 'seventh', 'dominant seventh', 'dom7', 'dominant7'):
    (M3, P5, m7),
    ('德国增六和弦', 'germansixth'): (M3, P5, A6),
    ('小大七和弦', 'minormajor7', 'minor major 7', 'mM7'): (m3, P5, M7),
    ('减三和弦', 'dim', 'o'): (m3, d5),
    ('减七和弦', 'dim7', 'o7'): (m3, d5, d7),
    ('半减七和弦', 'half-diminished7', 'ø7', 'ø', 'half-diminished', 'half-dim', 'm7b5'):
    (m3, d5, m7),
    ('增三和弦', 'aug', 'augmented', '+', 'aug3', '+3'): (M3, A5),
    ('增七和弦', 'aug7', 'augmented7', '+7'): (M3, A5, m7),
    ('增大七和弦', 'augmaj7', 'augmented-major7', '+maj7', 'augM7'): (M3, A5, M7),
    ('意大利增六和弦', 'aug6', 'augmented6', '+6', 'italian-sixth'): (M3, A6),
    ('法国增六和弦', 'frenchsixth'): (M3, d5, A6),
    ('增九和弦', 'aug9', '+9'): (M3, A5, m7, M9),
    ('挂四和弦', 'sus', 'sus4'): (P4, P5),
    ('挂二和弦', 'sus2'): (M2, P5),
    ('属九和弦', '9', 'dominant9', 'dominant-ninth', 'ninth'): (M3, P5, m7, M9),
    ('大九和弦', 'maj9', 'major-ninth', 'major9th', 'M9'): (M3, P5, M7, M9),
    ('小九和弦', 'm9', 'minor9', 'minor9th', '-9'): (m3, P5, m7, M9),
    ('增大九和弦', 'augmaj9', '+maj9', '+M9', 'augM9'): (M3, A5, M7, M9),
    ('大六和弦', 'add6', '6', 'sixth'): (M3, P5, M6),
    ('小六和弦', 'm6', 'minorsixth'): (m3, P5, M6),
    ('加二和弦', 'add2', '+2'): (M2, M3, P5),
    ('加九和弦', 'add9'): (M3, P5, M9),
    ('加小二和弦', 'madd2', 'm+2'): (M2, m3, P5),
    ('加小九和弦', 'madd9'): (m3, P5, M9),
    ('属七挂四和弦', '7sus4', '7sus'): (P4, P5, m7),
    ('属七挂二和弦', '7sus2'): (M2, P5, m7),
    ('大七挂四和弦', 'maj7sus4', 'maj7sus', 'M7sus4'): (P4, P5, M7),
    ('大七挂二和弦', 'maj7sus2', 'M7sus2'): (M2, P5, M7),
    ('属九挂四和弦', '9sus4', '9sus'): (P4, P5, m7, M9),
    ('属九挂二和弦', '9sus2'): (M2, P5, m7, M9),
    ('大九挂四和弦', 'maj9sus4', 'maj9sus', 'M9sus', 'M9sus4'): (P4, P5, M7, M9),
    ('属十一和弦', '11', 'dominant11', 'dominant 11'): (M3, P5, m7, M9, P11),
    ('大十一和弦', 'maj11', 'M11', 'eleventh', 'major 11', 'major eleventh'):
    (M3, P5, M7, M9, P11),
    ('小十一和弦', 'm11', 'minor eleventh', 'minor 11'): (m3, P5, m7, M9, P11),
    ('属十三和弦', '13', 'dominant13', 'dominant 13'): (M3, P5, m7, M9, P11, M13),
    ('大十三和弦', 'maj13', 'major 13', 'M13'): (M3, P5, M7, M9, P11, M13),
    ('小十三和弦', 'm13', 'minor 13'): (m3, P5, m7, M9, P11, M13),
    ('属十三挂四和弦', '13sus4', '13sus'): (P4, P5, m7, M9, M13),
    ('属十三挂二和弦', '13sus2'): (M2, P5, m7, P11, M13),
    ('大十三挂四和弦', 'maj13sus4', 'maj13sus', 'M13sus', 'M13sus4'):
    (P4, P5, M7, M9, M13),
    ('大十三挂二和弦', 'maj13sus2', 'M13sus2'): (M2, P5, M7, P11, M13),
    ('加四和弦', 'add4', '+4'): (M3, P4, P5),
    ('加小四和弦', 'madd4', 'm+4'): (m3, P4, P5),
    ('大七降五和弦', 'maj7b5', 'M7b5'): (M3, d5, M7),
    ('大七升十一和弦', 'maj7#11', 'M7#11'): (M3, P5, M7, A11),
    ('大九升十一和弦', 'maj9#11', 'M9#11'): (M3, P5, M7, M9, A11),
    ('六九和弦', '69', '6/9', 'add69'): (M3, P5, M6, M9),
    ('小六九和弦', 'm69', 'madd69'): (m3, P5, M6, M9),
    ('大六挂四和弦', '6sus4', '6sus'): (P4, P5, M6),
    ('大六挂二和弦', '6sus2'): (M2, P5, M6),
    ('强力和弦(五度和弦)', '5', 'power chord'): (P5, ),
    ('强力和弦(五度八度和弦)', '5(+octave)', 'power chord(with octave)'): (P5, P8),
    ('大十三升十一和弦', 'maj13#11', 'M13#11'): (M3, P5, M7, M9, A11, M13),
    ('属十三升十一和弦', '13#11'): (M3, P5, m7, M9, A11, M13),
    ('五度加九和弦', 'fifth_9th'): (P5, M9),
    ('小大九和弦', 'minormajor9', 'minor major 9', 'mM9'): (m3, P5, M7, M9),
    ('减大七和弦', 'dim(Maj7)'): (m3, d5, M7)
})

detectTypes = chordTypes.reverse(mode=1)

# musicpy


def to_text(self, show_degree=True, show_voicing=True, custom_mapping=None):
    if self.type == 'note':
        return f'音符 {self.note_name}'
    elif self.type == 'interval':
        return f'{self.root} 和 {self.interval_name}'
    elif self.type == 'chord':
        if self.chord_speciality == 'polychord':
            return '/'.join([
                f'[{i.to_text(show_degree=show_degree, show_voicing=show_voicing, custom_mapping=custom_mapping)}]'
                for i in self.polychords[::-1]
            ])
        else:
            current_chord = mp.C(self.get_root_position(),
                                 custom_mapping=custom_mapping)
            if self.altered:
                if show_degree:
                    altered_msg = ', '.join(self.altered)
                else:
                    current_alter = []
                    for i in self.altered:
                        if i[1:].isdigit():
                            current_degree = current_chord.interval_note(i[1:])
                            if current_degree is not None:
                                current_alter.append(i[0] +
                                                     current_degree.name)
                        else:
                            current_alter.append(i)
                    altered_msg = ', '.join(current_alter)
            else:
                altered_msg = ''
            if self.omit:
                if show_degree:
                    omit_msg = f' 省略 {", ".join([str(i) for i in self.omit])}'
                else:
                    current_omit = []
                    for i in self.omit:
                        if '/' in i:
                            i = i.split('/')[0]
                        if i in database.precise_degree_match:
                            current_degree = current_chord.interval_note(
                                i, mode=1)
                            if current_degree is not None:
                                current_omit.append(current_degree.name)
                        else:
                            current_omit.append(i)
                    omit_msg = f' 省略 {", ".join(current_omit)}'
            else:
                omit_msg = ''
            voicing_msg = f'排序 {self.voicing}' if self.voicing else ''
            non_chord_bass_note_msg = f'/{self.non_chord_bass_note}' if self.non_chord_bass_note else ''
            if self.chord_speciality == 'root position':
                result = f'{self.root}{self.chord_type}'
                if omit_msg:
                    result += omit_msg
            elif self.chord_speciality == 'inverted chord':
                result = f'{self.root}{self.chord_type}'
                if omit_msg:
                    result += omit_msg
                if self.omit is not None:
                    current_omit_chord = current_chord.omit(
                        [database.precise_degree_match[i] for i in self.omit],
                        mode=1)
                else:
                    current_omit_chord = current_chord
                result += f'/{current_omit_chord[self.inversion].name}'
            elif self.chord_speciality == 'chord voicings' or self.chord_speciality == 'altered chord':
                result = f'{self.root}{self.chord_type}'
                if omit_msg:
                    result += omit_msg
            if non_chord_bass_note_msg:
                result += non_chord_bass_note_msg
            if not show_voicing:
                other_msg = [altered_msg]
            else:
                other_msg = [altered_msg, voicing_msg]
            other_msg = [i for i in other_msg if i]
            if other_msg:
                result += ' ' + ' '.join(other_msg)
            return result


info_translate_dict = {
    'type': '类型',
    'note': '音符',
    'interval': '音程',
    'chord': '和弦',
    'root': '根音',
    'chord type': '和弦名称',
    'chord speciality': '和弦性质',
    'inversion': '转位',
    'omit': '省略音',
    'altered': '变化音',
    'non chord bass note': '和弦外音的最低音',
    'voicing': '和弦声位',
    'note name': '音符名称',
    'interval name': '音程名称',
    'polychords': '复合和弦',
    'root position': '原位和弦',
    'inverted chord': '转位和弦',
    'altered chord': '变化音和弦',
    'chord voicings': '和弦声位',
    'polychord': '复合和弦'
}


def show(self, **to_text_args):
    current_vars = vars(self)
    if self.type == 'note':
        current = '\n'.join([
            f'{info_translate_dict[i.replace("_", " ")]}: {info_translate_dict.get(current_vars[i], current_vars[i])}'
            for i in ['type', 'note_name']
        ])
    elif self.type == 'interval':
        current = '\n'.join([
            f'{info_translate_dict[i.replace("_", " ")]}: {info_translate_dict.get(current_vars[i], current_vars[i])}'
            for i in ['type', 'root', 'interval_name']
        ])
    elif self.type == 'chord':
        current = [
            f'{info_translate_dict["type"]}: {info_translate_dict[self.type]}'
        ] + [
            f'{info_translate_dict[i.replace("_", " ")]}: {info_translate_dict.get(j, j) if not isinstance(j, list) else j}'
            for i, j in current_vars.items() if i not in
            ['type', 'note_name', 'interval_name', 'highest_ratio']
        ]
        if self.chord_speciality == 'polychord':
            for i, each in enumerate(current):
                if each.startswith(f'{info_translate_dict["polychords"]}:'):
                    current[
                        i] = f'{info_translate_dict["polychords"]}: {[i.to_text(**to_text_args) for i in self.polychords]}'
                    break
        current = '\n'.join(current)
    return current


# browse

browse_language_dict = {
    'choose': "选择你想要播放的MIDI文件",
    'MIDI files': "MIDI文件",
    'go back': "返回",
    'choose MIDI file': "选择你想要播放的MIDI文件",
    'out of index': '这个轨道不存在',
    'cancel': "取消",
    'trackind': 'MIDI轨道序号',
    'from': '从',
    'to': '到',
    'show melody': '只显示主旋律',
    'show chord': '只显示和弦',
    'merge': '合并所有音轨',
    'file name': '文件名'
}

# ideal piano

ideal_piano_language_dict = {
    'sort': '排序',
    'current_midi_device': '请先进入MIDI键盘模式，按ctrl可以关掉我哦~',
    'changes': '已改变为',
    'reload': '重新加载设置',
    'load': '正在加载音源，请稍候...',
    'finished': '音源加载完成',
    'no MIDI input': 'MIDI设备id不存在，\n请右键点击MIDI KEYBOARD按钮选择一个MIDI设备',
    'pause': '已暂停, 按{unpause_key}键继续',
    'repeat': '音乐播放完毕, 按{repeat_key}键重新听一遍',
    'sample': '正在使用音频采样渲染当前MIDI文件，请稍等',
    'soundfont': '正在使用SoundFont渲染当前MIDI文件，请稍等',
    'type': '类型',
    'chord name': '和弦名称',
    'root': '根音',
    'note name': '音符名称',
    'interval name': '音程名称',
    'whole name': '完整名称',
    'other': '其他',
    'chord': '和弦',
    'note': '音符',
    'interval': '音程',
    'with': '和'
}
