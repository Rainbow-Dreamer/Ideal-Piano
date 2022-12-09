import random
from threading import Thread
import multiprocessing
import browse
import musicpy as mp
import musicpy.control as control
import json_module
from change_settings import config_window, change_parameter

piano_config_path = 'packages/piano_config.json'
piano_config = json_module.json_module(piano_config_path)

app = QtWidgets.QApplication(sys.argv)
del app

original_chord_type_func = [
    copy(mp.chord_type.to_text),
    copy(mp.chord_type.show)
]

if piano_config.language == 'English':
    from languages.en import language_patch
    current_custom_mapping = None
    current_custom_chord_types = None
elif piano_config.language == 'Chinese':
    from languages.cn import language_patch
    mp.chord_type.to_text = language_patch.to_text
    mp.chord_type.show = language_patch.show
    current_custom_mapping = [
        language_patch.INTERVAL, language_patch.detectTypes,
        language_patch.chordTypes
    ]
    current_custom_chord_types = current_custom_mapping[2]

key = pyglet.window.key
has_soundfont_plugins = True
note_display_mode = ['bars', 'bars drop', '']


def load(dic, path, file_format, volume, current_wavdic=None):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}/{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    if current_wavdic is not None:
        current_wavdic.append(wavedict)
    return wavedict


def load_sf2(dic, sf2, volume, current_wavdic=None):
    wavedict = {
        i: pygame.mixer.Sound(
            buffer=sf2.export_note(dic[i],
                                   duration=piano_config.sf2_duration,
                                   decay=piano_config.sf2_decay,
                                   volume=piano_config.sf2_volume,
                                   get_audio=True).raw_data)
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    if current_wavdic is not None:
        current_wavdic.append(wavedict)
    return wavedict


def get_image(img):
    return pyglet.image.load(img).get_texture()


def update(dt):
    pass


def send_midi_mute_all_sounds(current_player, mode=0):
    for i in range(piano_config.midi_channels_number):
        current_player.write_short(
            0xb0 | i, piano_config.mute_all_sounds_cc_number
            if mode == 0 else piano_config.stop_all_sounds_cc_number, 0)


def start_send_midi_event(event_list, current_event_counter,
                          current_output_port_num, midi_event_length,
                          current_send_midi_queue):
    pygame.midi.quit()
    pygame.midi.init()
    current_player = pygame.midi.Output(current_output_port_num)
    current_start_time = time.time()
    current_position_time = 0
    while True:
        if not current_send_midi_queue.empty():
            current_msg = current_send_midi_queue.get()
            if current_msg == 'pause':
                if piano_config.play_midi_reset_sounds:
                    send_midi_mute_all_sounds(current_player)
                pause_start = time.time()
                while True:
                    if not current_send_midi_queue.empty():
                        current_pause_msg = current_send_midi_queue.get()
                        if current_pause_msg == 'unpause':
                            current_start_time += (time.time() - pause_start)
                            break
                        elif isinstance(current_pause_msg, list):
                            if current_pause_msg[0] == 'set_position':
                                current_position_time = current_pause_msg[1]
                                for k, each in enumerate(event_list):
                                    if each.time == current_position_time:
                                        current_event_counter = k
                                        break
                                    elif each.time > current_position_time:
                                        current_event_counter = k - 1
                                        if current_event_counter < 0:
                                            current_event_counter = 0
                                        break
                                current_start_time = time.time()
            elif isinstance(current_msg, list):
                if current_msg[0] == 'set_position':
                    if piano_config.play_midi_reset_sounds:
                        send_midi_mute_all_sounds(current_player)
                    current_position_time = current_msg[1]
                    for k, each in enumerate(event_list):
                        if each.time == current_position_time:
                            current_event_counter = k
                            break
                        elif each.time > current_position_time:
                            current_event_counter = k - 1
                            if current_event_counter < 0:
                                current_event_counter = 0
                            break
                    current_start_time = time.time()
        current_time = time.time()
        past_time = current_time - current_start_time + current_position_time
        current_event = event_list[current_event_counter]
        if past_time >= current_event.time:
            mode = current_event.mode
            current_track = current_event.track
            if mode == 0:
                current_note = current_event.value
                current_channel = current_note.channel if current_note.channel is not None else channels[
                    current_event.track]
                current_player.note_on(note=current_note.degree,
                                       velocity=current_note.volume,
                                       channel=current_channel)
            elif mode == 1:
                current_note = current_event.value
                current_channel = current_note.channel if current_note.channel is not None else channels[
                    current_event.track]
                current_player.note_off(note=current_note.degree,
                                        channel=current_channel)
            elif mode == 2:
                current_player.set_instrument(
                    instrument_id=current_event.value,
                    channel=current_event.channel)
            elif mode == 3:
                current_channel = current_event.value.channel if current_event.value.channel is not None else channels[
                    current_event.track]
                current_player.pitch_bend(value=current_event.value.value,
                                          channel=current_channel)
            elif mode == 4:
                current_player.write_short(0xFF, 0x51,
                                           int(current_event.value))
            elif mode == 5:
                current_player.write_short(0xb0 | current_event.value.channel,
                                           current_event.value.control,
                                           current_event.value.value)
            elif mode == 6:
                current_player.write_short(0xc0 | current_event.value.channel,
                                           current_event.value.program)
            current_event_counter += 1
            if current_event_counter == midi_event_length:
                break


class ideal_piano_button:

    def __init__(self, img, x, y):
        self.img = get_image(img).get_transform()
        self.img.width /= piano_config.button_resize_num
        self.img.height /= piano_config.button_resize_num
        self.button = pyglet.sprite.Sprite(self.img, x=x, y=y)
        self.button.opacity = piano_config.button_opacity
        self.ranges = [x, x + self.button.width], [y, y + self.button.height]

    def get_range(self):
        height, width = self.button.height, self.button.width
        x, y = self.button.x, self.button.y
        return [x, x + width], [y, y + height]

    def inside(self, mouse_pos):
        range_x, range_y = self.get_range()
        return range_x[0] <= mouse_pos[0] <= range_x[1] and range_y[
            0] <= mouse_pos[1] <= range_y[1]

    def draw(self):
        self.button.draw()

    def mouse_press(self, window, button, mouse):
        return self.inside(window.mouse_pos) and button == mouse


class piano_window(pyglet.window.Window):

    def __init__(self):
        self.init_sf2()
        self.init_window()
        self.init_parameters()
        self.init_key_map()
        self.init_keys()
        self.init_screen()
        self.init_layers()
        self.init_screen_buttons()
        self.init_piano_keys()
        self.init_note_mode()
        self.init_screen_labels()
        self.init_music_analysis()
        self.init_progress_bar()
        self.push_handlers(on_resize=self.local_on_resize)

    def init_window(self):
        super(piano_window, self).__init__(
            *piano_config.screen_size,
            caption='Ideal Piano',
            resizable=True,
            file_drops=True if sys.platform != 'darwin' else False)
        self.icon = pyglet.image.load('resources/piano.ico')
        self.set_icon(self.icon)
        self.keyboard_handler = key.KeyStateHandler()
        self.push_handlers(self.keyboard_handler)
        self.current_screen_size = copy(piano_config.screen_size)

    def init_key_map(self):
        self.map_key_dict = {
            each.lower().lstrip('_'): value
            for each, value in key.__dict__.items() if isinstance(value, int)
        }
        self.map_key_dict_reverse = {
            j: i
            for i, j in self.map_key_dict.items()
        }
        self.map_key_dict_reverse[59] = ';'
        self.map_key_dict_reverse[39] = "'"
        self.map_key_dict_reverse[44] = ","
        self.map_key_dict_reverse[46] = "."
        self.map_key_dict_reverse[47] = '/'
        self.map_key_dict_reverse[91] = '['
        self.map_key_dict_reverse[93] = ']'
        self.map_key_dict_reverse[92] = '\\'
        self.map_key_dict_reverse[96] = '`'
        self.map_key_dict_reverse[45] = '-'
        self.map_key_dict_reverse[61] = '='
        self.map_key_dict_reverse[65288] = 'backspace'
        self.map_key_dict2 = {
            j: i
            for i, j in self.map_key_dict_reverse.items()
        }

    def init_keys(self):
        self.pause_key = self.map_key_dict.setdefault(piano_config.pause_key,
                                                      key.SPACE)
        self.repeat_key = self.map_key_dict.setdefault(piano_config.repeat_key,
                                                       key.LCTRL)
        self.unpause_key = self.map_key_dict.setdefault(
            piano_config.unpause_key, key.ENTER)
        self.config_key = self.map_key_dict.setdefault(piano_config.config_key,
                                                       key.LALT)

    def init_sf2(self, mode=0):
        if mode == 0:
            self.current_sf2_player = None
        if piano_config.play_use_soundfont or piano_config.use_soundfont:
            if 'rs' not in sys.modules:
                global rs, has_soundfont_plugins
                if has_soundfont_plugins:
                    try:
                        import sf2_loader as rs
                    except:
                        piano_config.use_soundfont = False
                        piano_config.play_use_soundfont = False
                        has_soundfont_plugins = False
                        self.use_soundfont_msg_box()
                else:
                    piano_config.use_soundfont = False
                    piano_config.play_use_soundfont = False
        if piano_config.play_use_soundfont:
            self.current_sf2 = rs.sf2_loader(piano_config.sf2_path)
            self.current_sf2.change(bank=piano_config.bank,
                                    preset=piano_config.preset)
        if piano_config.use_soundfont:
            if mode == 0:
                self.current_sf2_player = rs.sf2_player(piano_config.sf2_path)
            else:
                if self.current_sf2_player:
                    if piano_config.sf2_path != self.current_sf2_player.file[
                            -1]:
                        self.current_sf2_player.load(piano_config.sf2_path)
                else:
                    self.current_sf2_player = rs.sf2_player(
                        piano_config.sf2_path)

    def init_screen(self):
        self.screen_width, self.screen_height = piano_config.screen_size
        pygame.mixer.init(piano_config.frequency, piano_config.size,
                          piano_config.channel, piano_config.buffer)
        pygame.mixer.set_num_channels(piano_config.max_num_channels)
        try:
            background = get_image(piano_config.background_image)
        except:
            background = get_image('resources/white.png')
        if not piano_config.background_size:
            if piano_config.width_or_height_first:
                ratio_background = self.screen_width / background.width
                background.width = self.screen_width
                background.height *= ratio_background
            else:
                ratio_background = self.screen_height / background.height
                background.height = self.screen_height
                background.width *= ratio_background
        else:
            if not piano_config.background_fix_original_ratio:
                background.width, background.height = piano_config.background_size
            else:
                current_width, current_height = piano_config.background_size
                if piano_config.width_or_height_first:
                    ratio_background = current_width / background.width
                    background.width = current_width
                    background.height *= ratio_background
                else:
                    ratio_background = current_height / background.height
                    background.height = current_height
                    background.width *= ratio_background
        self.background = pyglet.sprite.Sprite(
            background,
            x=piano_config.background_place[0],
            y=piano_config.background_place[1])
        self.background.opacity = piano_config.background_opacity

    def init_layers(self):
        self.batch = pyglet.graphics.Batch()
        self.bottom_group = pyglet.graphics.OrderedGroup(0)
        self.piano_bg = pyglet.graphics.OrderedGroup(1)
        self.piano_key = pyglet.graphics.OrderedGroup(2)
        self.play_highlight = pyglet.graphics.OrderedGroup(3)
        self.piano_keys_note_name = pyglet.graphics.OrderedGroup(4)

    def init_note_mode(self):
        current_piano_engine.plays = []
        if piano_config.note_mode == 'bars drop':
            current_piano_engine.bars_drop_time = []
            distances = self.screen_height - self.piano_height
            self.bars_drop_interval = piano_config.bars_drop_interval
            if self.bars_drop_interval > 2:
                current_adjust_ratio = (piano_config.adjust_ratio /
                                        (self.bars_drop_interval / 2)) * 1.97
            else:
                current_adjust_ratio = piano_config.adjust_ratio
            self.bar_unit = piano_config.bar_unit / (self.bars_drop_interval /
                                                     2)
            self.bar_steps = piano_config.bar_steps
            self.drop_bar_steps = (
                distances / self.bars_drop_interval) / current_adjust_ratio
            self.init_drop_bar_steps = copy(self.drop_bar_steps)
        else:
            self.bar_steps = piano_config.bar_steps
            self.drop_bar_steps = piano_config.bar_steps
            self.init_drop_bar_steps = copy(self.drop_bar_steps)
            self.bars_drop_interval = piano_config.bars_drop_interval
            self.bar_unit = piano_config.bar_unit
        self.bar_hold_increase = piano_config.bar_hold_increase
        self.init_bar_unit = copy(self.bar_unit)
        self.bars_drop_place = piano_config.bars_drop_place

    def init_screen_buttons(self):
        if piano_config.language == 'Chinese':
            piano_config.go_back_image = 'packages/languages/cn/go_back.png'
            piano_config.self_play_image = 'packages/languages/cn/play.png'
            piano_config.self_midi_image = 'packages/languages/cn/midi_keyboard.png'
            piano_config.play_midi_image = 'packages/languages/cn/play_midi.png'
            piano_config.settings_image = 'packages/languages/cn/settings.png'
        if not os.path.exists(piano_config.go_back_image):
            piano_config.go_back_image = 'resources/go_back.png'
        if not os.path.exists(piano_config.self_play_image):
            piano_config.self_play_image = 'resources/play.png'
        if not os.path.exists(piano_config.self_midi_image):
            piano_config.self_midi_image = 'resources/play_midi.png'
        if not os.path.exists(piano_config.settings_image):
            piano_config.settings_image = 'resources/settings.png'
        self.go_back_button = ideal_piano_button(piano_config.go_back_image,
                                                 *piano_config.go_back_place)
        self.self_play_button = ideal_piano_button(
            piano_config.self_play_image, *piano_config.self_play_place)
        self.self_midi_button = ideal_piano_button(
            piano_config.self_midi_image, *piano_config.self_midi_place)
        self.play_midi_button = ideal_piano_button(
            piano_config.play_midi_image, *piano_config.play_midi_place)
        self.settings_button = ideal_piano_button(piano_config.settings_image,
                                                  *piano_config.settings_place)

    def init_screen_labels(self):
        if piano_config.fonts_file:
            pyglet.font.add_file(piano_config.fonts_file)
        if piano_config.fonts_path:
            pyglet.font.add_directory(piano_config.fonts_path)
        self.label = pyglet.text.Label('',
                                       font_name=piano_config.fonts,
                                       font_size=piano_config.fonts_size,
                                       bold=piano_config.bold,
                                       italic=piano_config.italic,
                                       dpi=piano_config.fonts_dpi,
                                       x=piano_config.label1_place[0],
                                       y=piano_config.label1_place[1],
                                       color=piano_config.message_color,
                                       anchor_x=piano_config.label_anchor_x,
                                       anchor_y=piano_config.label_anchor_y,
                                       multiline=True,
                                       width=piano_config.label_width)
        self.label2 = pyglet.text.Label('',
                                        font_name=piano_config.fonts,
                                        font_size=piano_config.fonts_size,
                                        bold=piano_config.bold,
                                        italic=piano_config.italic,
                                        dpi=piano_config.fonts_dpi,
                                        x=piano_config.label2_place[0],
                                        y=piano_config.label2_place[1],
                                        color=piano_config.message_color,
                                        anchor_x=piano_config.label_anchor_x,
                                        anchor_y=piano_config.label_anchor_y)
        self.label3 = pyglet.text.Label('',
                                        font_name=piano_config.fonts,
                                        font_size=piano_config.fonts_size,
                                        bold=piano_config.bold,
                                        italic=piano_config.italic,
                                        dpi=piano_config.fonts_dpi,
                                        x=piano_config.label3_place[0],
                                        y=piano_config.label3_place[1],
                                        color=piano_config.message_color,
                                        anchor_x=piano_config.label_anchor_x,
                                        anchor_y=piano_config.label_anchor_y)

        self.chord_details_label = pyglet.text.Label(
            '',
            font_name=piano_config.fonts,
            font_size=piano_config.chord_details_font_size,
            bold=piano_config.bold,
            italic=piano_config.italic,
            dpi=piano_config.fonts_dpi,
            x=piano_config.chord_details_label_place[0],
            y=piano_config.chord_details_label_place[1],
            color=piano_config.message_color,
            anchor_x=piano_config.chord_details_label_anchor_x,
            anchor_y=piano_config.chord_details_label_anchor_y,
            multiline=True,
            width=piano_config.chord_details_label_width)

        self.current_detect_key_label = pyglet.text.Label(
            '',
            font_name=piano_config.fonts,
            font_size=piano_config.current_detect_key_font_size,
            bold=piano_config.bold,
            italic=piano_config.italic,
            dpi=piano_config.fonts_dpi,
            x=piano_config.current_detect_key_label_place[0],
            y=piano_config.current_detect_key_label_place[1],
            color=piano_config.message_color,
            anchor_x=piano_config.current_detect_key_label_anchor_x,
            anchor_y=piano_config.current_detect_key_label_anchor_y,
            multiline=True,
            width=piano_config.current_detect_key_label_width)

    def init_music_analysis(self):
        self.music_analysis_list = []
        if piano_config.show_music_analysis:
            self.music_analysis_label = pyglet.text.Label(
                '',
                font_name=piano_config.fonts,
                font_size=piano_config.music_analysis_fonts_size,
                bold=piano_config.bold,
                italic=piano_config.italic,
                dpi=piano_config.fonts_dpi,
                x=piano_config.music_analysis_place[0],
                y=piano_config.music_analysis_place[1],
                color=piano_config.message_color,
                anchor_x=piano_config.label_anchor_x,
                anchor_y=piano_config.label_anchor_y,
                multiline=True,
                width=piano_config.music_analysis_width)
            if piano_config.music_analysis_file:
                try:
                    with open(piano_config.music_analysis_file,
                              encoding='utf-8') as f:
                        data = f.read()
                    lines = [i for i in data.split('\n\n') if i]
                    current_key = None
                    bar_counter = 0
                    for each in lines:
                        if each:
                            if each[:3] != 'key':
                                current = each.split('\n')
                                current_bar = current[0]
                                if current_bar[0] == '+':
                                    bar_counter += eval(current_bar[1:])
                                else:
                                    bar_counter = eval(current_bar) - 1
                                current_chords = '\n'.join(current[1:])
                                if current_key:
                                    current_chords = f'{piano_config.key_header}{current_key}\n' + current_chords
                                self.music_analysis_list.append(
                                    [bar_counter, current_chords])
                            else:
                                current_key = each.split('key: ')[1]
                except:
                    self.music_analysis_list = []

    def init_piano_keys(self):
        self.piano_height = piano_config.white_key_y + piano_config.white_key_height
        self.piano_keys = []
        self.initial_colors = []
        if piano_config.piano_background_image and os.path.exists(
                piano_config.piano_background_image):
            piano_background = get_image(piano_config.piano_background_image)
            if not piano_config.piano_size:
                ratio = self.screen_width / piano_background.width
                piano_background.width = self.screen_width
                piano_background.height *= ratio
            else:
                piano_background.width, piano_background.height = piano_config.piano_size
            self.piano_background_show = pyglet.sprite.Sprite(
                piano_background,
                x=0,
                y=0,
                batch=self.batch,
                group=self.piano_bg)
            self.piano_background_show.opacity = piano_config.piano_background_opacity
        else:
            piano_background = None

        for i in range(piano_config.white_keys_number):
            current_piano_key = pyglet.shapes.BorderedRectangle(
                x=piano_config.white_key_start_x +
                piano_config.white_key_interval * i,
                y=piano_config.white_key_y,
                width=piano_config.white_key_width,
                height=piano_config.white_key_height,
                color=piano_config.white_key_color,
                batch=self.batch,
                group=self.piano_key,
                border=piano_config.piano_key_border,
                border_color=piano_config.piano_key_border_color)
            current_piano_key.current_color = None
            current_piano_key.opacity = piano_config.white_key_opacity
            self.piano_keys.append(current_piano_key)
            self.initial_colors.append(
                (current_piano_key.x, piano_config.white_key_color))
        first_black_key = pyglet.shapes.BorderedRectangle(
            x=piano_config.black_key_first_x,
            y=piano_config.black_key_y,
            width=piano_config.black_key_width,
            height=piano_config.black_key_height,
            color=piano_config.black_key_color,
            batch=self.batch,
            group=self.piano_key,
            border=piano_config.piano_key_border,
            border_color=piano_config.piano_key_border_color)
        first_black_key.current_color = None
        first_black_key.opacity = piano_config.black_key_opacity
        self.piano_keys.append(first_black_key)
        self.initial_colors.append(
            (first_black_key.x, piano_config.black_key_color))
        current_start = piano_config.black_key_start_x
        for j in range(piano_config.black_keys_set_num):
            for k in piano_config.black_keys_set:
                current_start += k
                current_piano_key = pyglet.shapes.BorderedRectangle(
                    x=current_start,
                    y=piano_config.black_key_y,
                    width=piano_config.black_key_width,
                    height=piano_config.black_key_height,
                    color=piano_config.black_key_color,
                    batch=self.batch,
                    group=self.piano_key,
                    border=piano_config.piano_key_border,
                    border_color=piano_config.piano_key_border_color)
                current_piano_key.current_color = None
                current_piano_key.opacity = piano_config.black_key_opacity
                self.piano_keys.append(current_piano_key)
                self.initial_colors.append(
                    (current_start, piano_config.black_key_color))
            current_start += piano_config.black_keys_set_interval
        self.piano_keys.sort(key=lambda s: s.x)
        self.initial_colors.sort(key=lambda s: s[0])
        self.initial_colors = [t[1] for t in self.initial_colors]
        self.note_place = [(each.x, each.y) for each in self.piano_keys]
        self.note_num = len(self.note_place)
        if piano_config.show_note_name_on_piano_key:
            self.piano_keys_note_names_label = []
            current_piano_keys_note_names = [
                mp.degree_to_note(i + 21) for i in range(len(self.piano_keys))
            ]
            if piano_config.show_only_start_note_name:
                ind = [
                    i for i, each in enumerate(current_piano_keys_note_names)
                    if each.name == 'C'
                ]
            else:
                ind = [
                    i for i, each in enumerate(current_piano_keys_note_names)
                    if '#' not in each.name
                ]
            for each in ind:
                current_label = pyglet.text.Label(
                    str(current_piano_keys_note_names[each]),
                    font_name=piano_config.fonts,
                    font_size=piano_config.piano_key_note_name_font_size,
                    bold=piano_config.piano_key_note_name_bold,
                    italic=piano_config.piano_key_note_name_italic,
                    dpi=piano_config.dpi,
                    x=self.note_place[each][0] +
                    piano_config.piano_key_note_name_pad_x,
                    y=self.note_place[each][1] +
                    piano_config.piano_key_note_name_pad_y,
                    color=piano_config.piano_key_note_name_color,
                    batch=self.batch,
                    group=self.piano_keys_note_name)
                self.piano_keys_note_names_label.append(current_label)
            self.initial_note_names_place = [
                [i.x, i.y] for i in self.piano_keys_note_names_label
            ]
        self.bar_width = piano_config.bar_width
        self.bar_height = piano_config.bar_height
        self.bar_y = piano_config.bar_y

    def init_parameters(self):
        self.mouse_left = 1
        self.mouse_right = 4
        self.mouse_pos = 0, 0
        self.first_time = True
        self.message_label = False
        self.is_click = False
        self.mode_num = None
        self.func = None
        self.click_mode = None
        self.bar_offset_x = piano_config.bar_offset_x
        self.open_browse_window = False
        self.open_settings_window = False
        self.open_choose_midi_keyboard_window = False

    def init_language(self):
        global language_patch, current_custom_mapping, current_custom_chord_types
        if piano_config.language == 'English':
            from languages.en import language_patch
            importlib.reload(mp)
            mp.chord_type.to_text, mp.chord_type.show = original_chord_type_func
            current_custom_mapping = None
            current_custom_chord_types = None
        elif piano_config.language == 'Chinese':
            from languages.cn import language_patch
            mp.chord_type.to_text = language_patch.to_text
            mp.chord_type.show = language_patch.show
            current_custom_mapping = [
                language_patch.INTERVAL, language_patch.detectTypes,
                language_patch.chordTypes
            ]
            current_custom_chord_types = current_custom_mapping[2]

    def init_progress_bar(self):
        self.current_progress_bar = pyglet.shapes.BorderedRectangle(
            x=-2,
            y=0,
            width=2,
            height=piano_config.white_key_y,
            color=piano_config.progress_bar_color,
            batch=self.batch,
            group=self.piano_key)
        self.current_progress_bar.opacity = piano_config.progress_bar_opacity
        self.progress_bar_length = self.width

    def use_soundfont_msg_box(self):
        app = QtWidgets.QApplication(sys.argv)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle('Error')
        msg_box.setText(
            'It seems that FluidSynth is nozt installed on your computer, FluidSynth is required to play using SoundFont files as you set use_soundfont = True or play_use_soundfont = True, please install FluidSynth and then try to reopen again. You can use Ideal Piano as usual, as now the use soundfont config parameters will be set to False.'
        )
        msg_box.exec()

    def on_file_drop(self, x, y, paths):
        if paths:
            current_path = paths[0]
            import mimetypes
            current_type = mimetypes.guess_type(current_path)[0]
            if current_type:
                current_type, type_name = current_type.split('/')
                if current_type == 'image':
                    current_path = current_path.replace('\\', '/')
                    change_parameter('background_image', current_path,
                                     piano_config_path)
                    piano_config.background_image = current_path
                    self.init_screen()
                    self.local_on_resize(self.width, self.height, mode=1)
                elif 'mid' in type_name:
                    if self.click_mode is None:
                        init_result = current_piano_engine.init_midi_show(
                            current_path)
                        self.click_mode = 2
                        self.mode_num = 2
                        if init_result == 'back':
                            self.mode_num = 4
                        else:
                            self.func = current_piano_engine.mode_midi_show
                            self.not_first()
                            pyglet.clock.schedule_interval(
                                self.func, 1 / piano_config.fps)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = x, y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.go_back_button.mouse_press(
                self, button, mouse=self.mouse_left) and not self.first_time:
            self._go_back_func()
        if self.self_play_button.mouse_press(
                self, button, mouse=self.mouse_left) and self.first_time:
            self.click_mode = 0
        if self.self_midi_button.mouse_press(
                self, button, mouse=self.mouse_left) and self.first_time:
            self.click_mode = 1
        if self.self_midi_button.mouse_press(
                self, button, mouse=self.mouse_right) and self.first_time:
            self.open_midi_keyboard_right_click_menu()
        if self.play_midi_button.mouse_press(
                self, button, mouse=self.mouse_left) and self.first_time:
            self.click_mode = 2
        if self.settings_button.mouse_press(
                self, button, mouse=self.mouse_left) and self.first_time:
            self.open_settings()
        if self.mode_num == 2 and button == self.mouse_left and self.inside_progression_bar(
                x, y):
            if not current_piano_engine.finished:
                self.set_position(x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.mode_num == 2 and button == self.mouse_left and self.inside_progression_bar(
                x, y):
            if not current_piano_engine.finished:
                self.set_position(x + dx, y)

    def inside_progression_bar(self, x, y):
        return self.current_progress_bar.x <= x <= self.current_progress_bar.x + self.progress_bar_length and self.current_progress_bar.y <= y <= self.current_progress_bar.y + self.current_progress_bar.height

    def set_position(self, x, y):
        current_percentage = x / self.progress_bar_length
        current_position = current_piano_engine.stop_time * current_percentage
        current_piano_engine._midi_show_set_position(current_position)

    def on_draw(self):
        self.clear()
        self.background.draw()
        if self.batch:
            self.batch.draw()
        self.go_back_button.draw()
        if self.first_time:
            self._draw_window_first_time()
        else:
            self._draw_window()

    def local_on_resize(self, width, height, mode=0):
        if piano_config.resize_screen:
            if mode == 0 and width == self.current_screen_size[
                    0] and height == self.current_screen_size[1]:
                return
            self.current_screen_size[0] = width
            self.current_screen_size[1] = height
            scale_x = width / piano_config.background_size[0]
            scale_y = height / piano_config.background_size[1]
            self.background.scale_x = scale_x
            self.background.scale_y = scale_y
            self.piano_background_show.scale_x = scale_x
            self.piano_background_show.scale_y = scale_y
            current_white_key_interval = piano_config.white_key_interval * scale_x
            white_key_counter = 0
            black_key_counter = 0
            black_keys_set_num = len(piano_config.black_keys_set)
            black_keys_set_length = sum(piano_config.black_keys_set)
            current_piano_engine.reset_all_piano_keys()
            if self.mode_num == 0:
                current_piano_engine._pc_clear_all_bars()
            elif self.mode_num == 1:
                current_piano_engine._midi_keyboard_clear_all_bars()
            elif self.mode_num == 2:
                current_piano_engine._midi_show_clear_all_bars_drop()
            for each in self.piano_keys:
                if each.color == piano_config.white_key_color:
                    each.width = piano_config.white_key_width * scale_x
                    each.height = piano_config.white_key_height * scale_y
                    each.x = piano_config.white_key_start_x + current_white_key_interval * white_key_counter
                    each.y = piano_config.white_key_y * scale_y
                    white_key_counter += 1
                elif each.color == piano_config.black_key_color:
                    each.width = piano_config.black_key_width * scale_x
                    each.height = piano_config.black_key_height * scale_y
                    if black_key_counter == 0:
                        each.x = piano_config.black_key_first_x * scale_x
                        each.y = piano_config.black_key_y * scale_y
                    else:
                        current_black_key_set_num, current_black_key_ind = divmod(
                            black_key_counter - 1, black_keys_set_num)
                        each.x = (piano_config.black_key_start_x +
                                  (black_keys_set_length +
                                   piano_config.black_keys_set_interval) *
                                  current_black_key_set_num +
                                  sum(piano_config.
                                      black_keys_set[:current_black_key_ind +
                                                     1])) * scale_x
                        each.y = piano_config.black_key_y * scale_y
                    black_key_counter += 1
            self.note_place = [(each.x, each.y) for each in self.piano_keys]
            self.piano_height = (piano_config.white_key_y +
                                 piano_config.white_key_height) * scale_y
            self.bars_drop_place = piano_config.bars_drop_place * scale_y
            self.bar_width = piano_config.bar_width * scale_x
            self.bar_height = piano_config.bar_height * scale_y
            self.bar_y = piano_config.bar_y * scale_y
            self.bar_offset_x = piano_config.bar_offset_x * scale_x
            self.bar_steps = piano_config.bar_steps * scale_y
            self.drop_bar_steps = self.init_drop_bar_steps * scale_y
            self.bar_hold_increase = piano_config.bar_hold_increase * scale_y
            self.bar_unit = self.init_bar_unit * scale_y

            self.go_back_button.button.x = piano_config.go_back_place[
                0] * scale_x
            self.go_back_button.button.y = piano_config.go_back_place[
                1] * scale_y
            self.go_back_button.button.scale_x = scale_x
            self.go_back_button.button.scale_y = scale_y

            self.self_play_button.button.x = piano_config.self_play_place[
                0] * scale_x
            self.self_play_button.button.y = piano_config.self_play_place[
                1] * scale_y
            self.self_play_button.button.scale_x = scale_x
            self.self_play_button.button.scale_y = scale_y

            self.self_midi_button.button.x = piano_config.self_midi_place[
                0] * scale_x
            self.self_midi_button.button.y = piano_config.self_midi_place[
                1] * scale_y
            self.self_midi_button.button.scale_x = scale_x
            self.self_midi_button.button.scale_y = scale_y

            self.play_midi_button.button.x = piano_config.play_midi_place[
                0] * scale_x
            self.play_midi_button.button.y = piano_config.play_midi_place[
                1] * scale_y
            self.play_midi_button.button.scale_x = scale_x
            self.play_midi_button.button.scale_y = scale_y

            self.settings_button.button.x = piano_config.settings_place[
                0] * scale_x
            self.settings_button.button.y = piano_config.settings_place[
                1] * scale_y
            self.settings_button.button.scale_x = scale_x
            self.settings_button.button.scale_y = scale_y

            if piano_config.show_notes:
                self.label.x = piano_config.label1_place[0] * scale_x
                self.label.y = piano_config.label1_place[1] * scale_y
            if piano_config.show_chord:
                self.label2.x = piano_config.label2_place[0] * scale_x
                self.label2.y = piano_config.label2_place[1] * scale_y
            if self.message_label:
                self.label3.x = piano_config.label3_place[0] * scale_x
                self.label3.y = piano_config.label3_place[1] * scale_y
            if piano_config.show_chord_details:
                self.chord_details_label.x = piano_config.chord_details_label_place[
                    0] * scale_x
                self.chord_details_label.y = piano_config.chord_details_label_place[
                    1] * scale_y
            if piano_config.show_current_detect_key:
                self.current_detect_key_label.x = piano_config.current_detect_key_label_place[
                    0] * scale_x
                self.current_detect_key_label.y = piano_config.current_detect_key_label_place[
                    1] * scale_y

            if piano_config.show_note_name_on_piano_key:
                for i, each in enumerate(self.piano_keys_note_names_label):
                    current_place = self.initial_note_names_place[i]
                    each.x = current_place[0] * scale_x
                    each.y = current_place[1] * scale_y
            self.current_progress_bar.height = piano_config.white_key_y * scale_y
            self.progress_bar_length = self.width

    def _go_back_func(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        if self.mode_num in [0, 1, 2]:
            pyglet.clock.unschedule(self.func)
            if current_piano_engine.plays:
                current_piano_engine.plays.clear()
            if self.mode_num == 0:
                if current_piano_engine.still_hold_pc:
                    current_piano_engine.still_hold_pc.clear()
            elif self.mode_num == 1:
                piano_config.delay_only_read_current = True
            elif self.mode_num == 2:
                pyglet.clock.unschedule(current_piano_engine.midi_file_play)
                pyglet.clock.unschedule(
                    current_piano_engine.
                    _midi_show_playing_read_pc_keyboard_key)
                pyglet.clock.unschedule(
                    current_piano_engine.
                    _midi_show_playing_read_pc_move_progress_key)
                pyglet.clock.unschedule(
                    current_piano_engine._midi_show_update_notes_text)
                pyglet.clock.unschedule(
                    current_piano_engine._midi_show_finished)
                current_piano_engine.counter = 0
                if piano_config.show_music_analysis:
                    self.music_analysis_label.text = ''
                if piano_config.use_soundfont:
                    if self.current_sf2_player.playing:
                        self.current_sf2_player.stop()
                current_piano_engine.current_hit_key_notes.clear()
                current_piano_window.current_progress_bar.width = 2
                if not piano_config.use_soundfont:
                    try:
                        current_piano_engine.current_send_midi_event_process.terminate(
                        )
                    except:
                        pass
                else:
                    pyglet.clock.unschedule(
                        current_piano_engine.start_play_sf2)
        self.is_click = True
        self.click_mode = None
        if piano_config.note_mode in note_display_mode:
            current_piano_engine.still_hold.clear()
            current_piano_engine.bars_drop_time.clear()
        for k in range(len(self.piano_keys)):
            self.piano_keys[k].color = self.initial_colors[k]
        self.label3.text = ''
        if current_piano_engine.detect_key_info:
            current_piano_engine.detect_key_info.clear()
            current_piano_engine.detect_key_info_ind = 0

    def _draw_window_first_time(self):
        self.self_play_button.draw()
        self.self_midi_button.draw()
        self.play_midi_button.draw()
        self.settings_button.draw()
        if self.mode_num is None:
            self._main_window_read_click_mode()
        else:
            self._main_window_enter_mode()

    def _main_window_read_click_mode(self):
        if self.keyboard_handler[self.config_key] and self.keyboard_handler[
                key.S]:
            self.open_settings()
        if self.keyboard_handler[self.config_key] and self.keyboard_handler[
                key.R]:
            self.label.text = language_patch.ideal_piano_language_dict[
                'reload']
            self.label.draw()
            self.flip()
            self.reload_settings()
        if self.click_mode == 0:
            self.mode_num = 0
            self.label.text = language_patch.ideal_piano_language_dict['load']
            self.label.draw()
        elif self.click_mode == 1:
            self.mode_num = 1
            self.label.text = language_patch.ideal_piano_language_dict['load']
            self.label.draw()
        elif self.click_mode == 2:
            self.mode_num = 2

    def _main_window_enter_mode(self):
        if self.mode_num == 0:
            self.not_first()
            current_piano_engine.init_self_pc()
        elif self.mode_num == 1:
            self.not_first()
            current_piano_engine.init_self_midi()
        elif self.mode_num == 2:
            if not self.open_browse_window:
                init_result = current_piano_engine.init_midi_show()
                if init_result == 'back':
                    self.mode_num = 4
                else:
                    self.func = current_piano_engine.mode_midi_show
                    self.not_first()
                    pyglet.clock.schedule_interval(self.func,
                                                   1 / piano_config.fps)
                    pyglet.clock.schedule_interval(
                        current_piano_engine.
                        _midi_show_playing_read_pc_keyboard_key, 0.1)
                    pyglet.clock.schedule_interval(
                        current_piano_engine.
                        _midi_show_playing_read_pc_move_progress_key, 0.1)
        elif self.mode_num == 3:
            time.sleep(2)
            self.label.text = ''
            self.mode_num = None
        elif self.mode_num == 4:
            self.label.text = ''
            self.mode_num = None
            self.reset_click_mode()

    def _draw_window(self):
        if self.is_click:
            self.is_click = False
            self.not_first()
            self.label.text = ''
            self.label2.text = ''

            pyglet.clock.unschedule(self.func)
            self.mode_num = None
        self.label.draw()
        self.label2.draw()
        if piano_config.show_chord_details:
            self.chord_details_label.draw()
        if piano_config.show_current_detect_key:
            self.current_detect_key_label.draw()
        if self.message_label:
            self.label3.draw()
        if piano_config.show_music_analysis:
            self.music_analysis_label.draw()

    def redraw(self):
        self.clear()
        self.background.draw()
        if self.batch:
            self.batch.draw()
        self.go_back_button.draw()
        self.label2.draw()
        if piano_config.show_chord_details:
            self.chord_details_label.draw()
        if piano_config.show_current_detect_key:
            self.current_detect_key_label.draw()
        if self.message_label:
            self.label3.draw()
        if piano_config.show_music_analysis:
            self.music_analysis_label.draw()

    def reset_click_mode(self):
        self.click_mode = None

    def not_first(self):
        self.first_time = not self.first_time

    def open_settings(self):
        if not self.open_settings_window:
            self.open_settings_window = True
            self.keyboard_handler[self.config_key] = False
            self.keyboard_handler[key.S] = False
            os.chdir(abs_path)
            app = QtWidgets.QApplication(sys.argv)
            dpi = (app.screens()[0]).logicalDotsPerInch()
            current_config_window = config_window(
                dpi=dpi, config_path=piano_config_path)
            app.exec()
            del app
            self.open_settings_window = False
            self.reload_settings()

    def open_midi_keyboard_right_click_menu(self):
        if not self.open_choose_midi_keyboard_window:
            self.open_choose_midi_keyboard_window = True
            app = QtWidgets.QApplication(sys.argv)
            dpi = (app.screens()[0]).logicalDotsPerInch()
            current_midi_keyboard_window = browse.midi_keyboard_window(dpi=dpi)
            app.exec()
            del app
            self.open_choose_midi_keyboard_window = False
            global piano_config
            piano_config = json_module.json_module(piano_config_path)

    def reload_settings(self):
        global piano_config
        piano_config = json_module.json_module(piano_config_path)
        current_piano_engine.notedic = piano_config.key_settings
        self.width = piano_config.screen_size[0]
        self.height = piano_config.screen_size[1]
        self.current_screen_size = copy(piano_config.screen_size)
        self.init_parameters()
        self.init_language()
        self.init_keys()
        self.init_sf2(1)
        self.init_screen()
        self.init_layers()
        self.init_screen_buttons()
        self.init_piano_keys()
        self.init_note_mode()
        self.init_screen_labels()
        self.init_music_analysis()
        self.init_progress_bar()
        self.local_on_resize(self.width, self.height, mode=1)


class piano_engine:

    def __init__(self):
        self.init_parameters()

    def init_parameters(self):
        self.notedic = piano_config.key_settings
        self.currentchord = mp.chord([])
        self.last_time_currentchord = None
        self.last_time_chordtype = None
        self.still_hold_pc = []
        self.still_hold = []
        self.paused = False
        self.pause_start = 0
        self.bars_drop_time = []
        self.plays = []
        self.midi_device_load = False
        self.device = None
        self.play_midi_file = False
        self.sostenuto_pedal_on = False
        self.soft_pedal_volume_ratio = 1
        self.detect_key_info = []
        self.detect_key_info_ind = 0
        self.current_output_port_num = None
        self.current_hit_key_notes = []

    def has_load(self, change):
        self.midi_device_load = change

    def configkey(self, current_key):
        return current_piano_window.keyboard_handler[
            current_piano_window.
            config_key] and current_piano_window.keyboard_handler[
                current_piano_window.map_key_dict2[current_key]]

    def configshow(self, content):
        current_piano_window.label.text = str(content)

    def switchs(self, current_key, name):
        if self.configkey(current_key):
            setattr(piano_config, name, not getattr(piano_config, name))
            self.configshow(
                f'{name} {language_patch.ideal_piano_language_dict["changes"]} {getattr(piano_config, name)}'
            )

    def detect_config(self):
        if self.configkey(piano_config.volume_up):
            if piano_config.global_volume + piano_config.volume_change_unit <= 1:
                piano_config.global_volume += piano_config.volume_change_unit
            else:
                piano_config.global_volume = 1
            [
                self.wavdic[j].set_volume(piano_config.global_volume)
                for j in self.wavdic
            ]
            self.configshow(
                f'volume up to {int(piano_config.global_volume*100)}%')
        if self.configkey(piano_config.volume_down):
            if piano_config.global_volume - piano_config.volume_change_unit >= 0:
                piano_config.global_volume -= piano_config.volume_change_unit
            else:
                piano_config.global_volume = 0
            [
                self.wavdic[j].set_volume(piano_config.global_volume)
                for j in self.wavdic
            ]
            self.configshow(
                f'volume down to {int(piano_config.global_volume*100)}%')
        self.switchs(piano_config.change_delay, 'delay')
        self.switchs(piano_config.change_read_current,
                     'delay_only_read_current')
        self.switchs(piano_config.change_pause_key_clear_notes,
                     'pause_key_clear_notes')
        if piano_config.play_use_soundfont:
            self.detect_sf2_config()

    def detect_sf2_config(self, mode=0):
        current_sf2 = current_piano_window.current_sf2
        if self.configkey('1'):
            if current_sf2.current_preset != 0:
                self._change_sf2_instrument(-1, audio_mode=mode)
        if self.configkey('2'):
            self._change_sf2_instrument(1, audio_mode=mode)
        if self.configkey('3'):
            if current_sf2.current_bank != 0:
                self._change_sf2_instrument(-1, 1, audio_mode=mode)
        if self.configkey('4'):
            self._change_sf2_instrument(1, 1, audio_mode=mode)

    def _change_sf2_instrument(self, step, mode=0, audio_mode=0):
        current_sf2 = current_piano_window.current_sf2
        if mode == 0:
            current_change = current_sf2.change(
                preset=current_sf2.current_preset + step, correct=False)
            current_preset = f'{current_sf2.current_preset} {current_sf2.get_current_instrument()}' if current_change != -1 else f'{current_sf2.current_preset} No preset'
            current_piano_window.redraw()
            current_piano_window.label.text = f'Change SoundFont preset to {current_preset}'
            current_piano_window.label.draw()
            current_piano_window.flip()
            if current_change != -1:
                if audio_mode == 0:
                    self.wavdic = load_sf2(self.notedic, current_sf2,
                                           piano_config.global_volume)
                else:
                    notenames = os.listdir(piano_config.sound_path)
                    notenames = [x[:x.index('.')] for x in notenames]
                    self.wavdic = load_sf2({i: i
                                            for i in notenames}, current_sf2,
                                           piano_config.global_volume)
        else:
            current_sf2.change_bank(current_sf2.current_bank + step)
            current_piano_window.redraw()
            current_piano_window.label.text = f'Change SoundFont bank to {current_sf2.current_bank}'
            current_piano_window.label.draw()
            current_piano_window.flip()

    def midi_file_play(self):
        if piano_config.use_soundfont:
            if piano_config.sf2_mode == 1:
                current_midi_file = current_piano_window.current_sf2_player.current_midi_file
                current_piano_window.current_sf2_player.synth.delete()
                current_piano_window.current_sf2_player = rs.sf2_player(
                    piano_config.sf2_path)
                current_piano_window.current_sf2_player.current_midi_file = current_midi_file
            self.current_ticks_per_beat = mp.get_ticks_per_beat(
                current_piano_window.current_sf2_player.current_midi_file)
            current_use_soundfont_delay_time = piano_config.use_soundfont_delay_time if piano_config.note_mode == 'bars drop' else 0
            pyglet.clock.schedule_once(
                self.start_play_sf2, current_piano_window.bars_drop_interval +
                current_use_soundfont_delay_time)
        else:
            self.current_send_midi_queue = multiprocessing.Queue()
            self.current_send_midi_event_process = multiprocessing.Process(
                target=start_send_midi_event,
                args=(self.event_list, 0, self.current_output_port_num,
                      self.midi_event_length, self.current_send_midi_queue))
            self.current_send_midi_event_process.daemon = True
            current_send_midi_event_thread = Thread(
                target=self.current_send_midi_event_process.start, daemon=True)
            current_send_midi_event_thread.start()

    def start_play_sf2(self, dt):
        current_piano_window.current_sf2_player.play_midi_file(
            current_piano_window.current_sf2_player.current_midi_file)

    def piano_key_reset(self, dt, each):
        current_piano_window.piano_keys[
            each.degree -
            21].color = current_piano_window.initial_colors[each.degree - 21]

    def reset_all_piano_keys(self):
        for i, each in enumerate(current_piano_window.piano_keys):
            each.color = current_piano_window.initial_colors[i]

    def _detect_chord(self, current_chord):
        if not isinstance(current_chord, mp.chord):
            current_chord = mp.chord(current_chord)
        current_chord_info = current_chord.info(
            change_from_first=piano_config.change_from_first,
            original_first=piano_config.original_first,
            same_note_special=piano_config.same_note_special,
            whole_detect=piano_config.whole_detect,
            poly_chord_first=piano_config.poly_chord_first,
            show_degree=piano_config.show_degree,
            custom_mapping=current_custom_mapping)
        if current_chord_info is None:
            return
        current_dict = language_patch.ideal_piano_language_dict
        if current_chord_info.type == 'chord':
            current_info = current_chord_info.to_text(
                show_degree=piano_config.show_degree,
                custom_mapping=current_custom_chord_types,
                show_voicing=not piano_config.sort_invisible)
            if piano_config.show_chord_accidentals == 'flat':
                current_chord_root = current_chord_info.root
                if '#' in current_chord_root:
                    new_current_chord_root = (~mp.N(current_chord_root)).name
                    current_info = current_info.replace(
                        current_chord_root, new_current_chord_root)
        elif current_chord_info.type == 'note':
            current_note = current_chord_info.note_name
            if piano_config.show_chord_accidentals == 'flat':
                if '#' in current_note:
                    new_current_note = ~mp.N(current_note)
                    current_info = f'{current_dict["note"]} {new_current_note}'
            else:
                current_info = f'{current_dict["note"]} {current_note}'
        elif current_chord_info.type == 'interval':
            current_root = current_chord_info.root
            if piano_config.show_chord_accidentals == 'flat':
                if '#' in current_root:
                    new_current_root = (~mp.N(current_root)).name
                    current_info = f'{new_current_root} {current_dict["with"]} {current_chord_info.interval_name}'
            else:
                current_info = f'{current_root} {current_dict["with"]} {current_chord_info.interval_name}'
        if piano_config.show_chord_details:
            current_piano_window.chord_details_label.text = current_chord_info.show(
                custom_mapping=current_custom_chord_types)
        if piano_config.show_current_detect_key:
            if piano_config.current_detect_key_limit is not None and len(
                    self.current_play_chords
            ) > piano_config.current_detect_key_limit:
                self.current_play_chords = mp.chord([])
            self.current_play_chords |= current_chord
            note_count = self.current_play_chords.count_appear(sort=True)
            current_detect_key_text = ''
            if piano_config.current_detect_key_algorithm == 0:
                current_detect_key = mp.alg.detect_scale(
                    self.current_play_chords,
                    most_appear_num=piano_config.
                    current_detect_key_most_appear_num,
                    major_minor_preference=piano_config.
                    current_detect_key_major_minor_preference)
                current_detect_key_text = current_detect_key
            elif piano_config.current_detect_key_algorithm == 1:
                current_detect_key = mp.alg.detect_scale2(
                    self.current_play_chords,
                    most_appear_num=piano_config.
                    current_detect_key_most_appear_num,
                    major_minor_preference=piano_config.
                    current_detect_key_major_minor_preference)
                current_detect_key_text = f'most likely scales: {current_detect_key}'
            elif piano_config.current_detect_key_algorithm == 2:
                if current_piano_window.mode_num == 2:
                    if self.detect_key_info:
                        for each in self.detect_key_info:
                            current_range, current_keys = each
                            if current_range[
                                    0] <= self.current_past_time <= current_range[
                                        1]:
                                current_detect_key_text = f'most likely scales: {current_keys}'
                                break
            if piano_config.current_detect_key_show_note_count:
                current_detect_key_text = f'note count: {note_count} / {len(self.current_play_chords)}\n\n{current_detect_key_text}'
            current_piano_window.current_detect_key_label.text = current_detect_key_text
        return current_info

    def init_self_pc(self):
        if not piano_config.play_use_soundfont:
            current_wavdic = []
            current_thread = Thread(
                target=load,
                args=(self.notedic, piano_config.sound_path,
                      piano_config.sound_format, piano_config.global_volume,
                      current_wavdic),
                daemon=True)
            current_thread.start()
        else:
            current_wavdic = []
            current_thread = Thread(
                target=load_sf2,
                args=(self.notedic, current_piano_window.current_sf2,
                      piano_config.global_volume, current_wavdic),
                daemon=True)
            current_thread.start()
        self.wait_self_pc_load(current_wavdic)

    def wait_self_pc_load(self, current_wavdic):
        if current_piano_window.click_mode is None:
            return
        if not current_wavdic:
            pyglet.clock.schedule_once(
                lambda dt: self.wait_self_pc_load(current_wavdic), 0.2)
        else:
            if current_piano_window.click_mode is None:
                return
            self.wavdic = current_wavdic[0]
            self.last = []
            self.changed = False
            if piano_config.delay:
                self.stillplay = []
            self.lastshow = None
            if piano_config.show_current_detect_key:
                self.current_play_chords = mp.chord([])
                current_piano_window.current_detect_key_label.text = ''

            current_piano_window.label.text = language_patch.ideal_piano_language_dict[
                'finished']
            current_piano_window.label.draw()
            current_piano_window.func = current_piano_engine.mode_self_pc
            pyglet.clock.schedule_interval(current_piano_window.func,
                                           1 / piano_config.fps)

    def init_self_midi(self):
        try:
            if not self.midi_device_load:
                self.device = None
                self.has_load(True)
                pygame.midi.quit()
                pygame.midi.init()
                self.device = pygame.midi.Input(piano_config.midi_device_id)
            else:
                if self.device:
                    self.device.close()
                    pygame.midi.quit()
                    pygame.midi.init()
                    self.device = pygame.midi.Input(
                        piano_config.midi_device_id)
            notenames = os.listdir(piano_config.sound_path)
            notenames = [x[:x.index('.')] for x in notenames]
            if piano_config.load_sound:
                if not piano_config.play_use_soundfont:
                    current_wavdic = []
                    current_thread = Thread(target=load,
                                            args=({i: i
                                                   for i in notenames
                                                   }, piano_config.sound_path,
                                                  piano_config.sound_format,
                                                  piano_config.global_volume,
                                                  current_wavdic),
                                            daemon=True)
                    current_thread.start()
                else:
                    current_wavdic = []
                    current_thread = Thread(
                        target=load_sf2,
                        args=({i: i
                               for i in notenames
                               }, current_piano_window.current_sf2,
                              piano_config.global_volume, current_wavdic),
                        daemon=True)
                    current_thread.start()
                self.wait_self_midi_load(current_wavdic)
            self.current_play = []
            self.stillplay = []
            self.last = self.current_play.copy()
            self.sostenuto_pedal_on = False
            self.soft_pedal_volume_ratio = 1
            if piano_config.show_current_detect_key:
                self.current_play_chords = mp.chord([])
                current_piano_window.current_detect_key_label.text = ''
        except Exception as e:
            self.has_load(False)
            pygame.midi.quit()
            current_piano_window.label.text = language_patch.ideal_piano_language_dict[
                'no MIDI input']
            current_piano_window.mode_num = 3
            current_piano_window.reset_click_mode()
            current_piano_window.label.draw()

    def wait_self_midi_load(self, current_wavdic):
        if current_piano_window.click_mode is None:
            return
        if not current_wavdic:
            pyglet.clock.schedule_once(
                lambda dt: self.wait_self_midi_load(current_wavdic), 0.2)
        else:
            if current_piano_window.click_mode is None:
                return
            self.wavdic = current_wavdic[0]
            if not self.device:
                current_piano_window.label.text = language_patch.ideal_piano_language_dict[
                    'no MIDI input']
                current_piano_window.mode_num = 3
                current_piano_window.reset_click_mode()
                current_piano_window.label.draw()
            else:
                current_piano_window.label.text = language_patch.ideal_piano_language_dict[
                    'finished']
                current_piano_window.label.draw()
                current_piano_window.func = self.mode_self_midi
                pyglet.clock.schedule_interval(current_piano_window.func,
                                               1 / piano_config.fps)

    def init_midi_show(self, file_name=None):
        current_piano_window.open_browse_window = True
        current_setup = browse.setup(language_patch.browse_language_dict,
                                     file_name=file_name)
        current_piano_window.open_browse_window = False
        self.path = current_setup.file_path
        self.action = current_setup.action
        read_result = current_setup.read_result
        self.sheetlen = current_setup.sheetlen
        set_bpm = current_setup.set_bpm
        self.show_mode = current_setup.show_mode
        self.if_merge = current_setup.if_merge
        if self.action == 1:
            self.action = 0
            return 'back'
        if self.path and read_result:
            if read_result != 'error':
                self.musicsheet, self.bpm, start_time, actual_start_time, drum_tracks, self.current_piece = read_result
                self.musicsheet, new_start_time = self.musicsheet.pitch_filter(
                    *piano_config.pitch_range)
                start_time += new_start_time
                self.sheetlen = len(self.musicsheet)
                if self.sheetlen == 0:
                    return 'back'
                if set_bpm:
                    self.bpm = float(set_bpm)
                    if drum_tracks:
                        current_musicsheet = copy(self.musicsheet)
                        current_musicsheet.start_time = 0
                        for each in drum_tracks:
                            current_musicsheet &= (each.content,
                                                   each.start_time -
                                                   start_time)
                        drum_tracks.clear()
                    else:
                        current_musicsheet = self.musicsheet
                    mp.write(current_musicsheet,
                             bpm=self.bpm,
                             start_time=actual_start_time,
                             name='temp.mid')
                    self.path = 'temp.mid'
            else:
                return 'back'
        else:
            return 'back'

        if self.show_mode != 0:
            current_melody, current_chord = mp.alg.split_all(
                current_chord=self.musicsheet,
                mode='chord',
                melody_tol=piano_config.melody_tol,
                chord_tol=piano_config.chord_tol,
                get_off_overlap_notes=piano_config.get_off_overlap_notes,
                average_degree_length=piano_config.average_degree_length,
                melody_degree_tol=piano_config.melody_degree_tol)
            shift = current_chord.start_time - current_melody.start_time
            if self.show_mode == 1:
                self.musicsheet = current_melody
                if shift < 0:
                    start_time += abs(shift)
            elif self.show_mode == 2:
                self.musicsheet = current_chord
                if shift >= 0:
                    start_time += shift
            self.sheetlen = len(self.musicsheet)
            if self.sheetlen == 0:
                return 'back'
            if self.show_mode == 2 and drum_tracks:
                current_musicsheet = copy(self.musicsheet)
                current_musicsheet.start_time = 0
                for each in drum_tracks:
                    current_musicsheet &= (each.content,
                                           each.start_time - start_time)
                drum_tracks.clear()
            else:
                current_musicsheet = self.musicsheet
            mp.write(current_musicsheet,
                     bpm=self.bpm,
                     start_time=start_time,
                     name='temp.mid')
            self.path = 'temp.mid'
        pygame.mixer.set_num_channels(self.sheetlen)
        self.wholenotes = self.musicsheet.notes
        self.unit_time = 4 * 60 / self.bpm
        self.musicsheet.start_time = start_time
        self.musicsheet.actual_start_time = actual_start_time

        if piano_config.show_current_detect_key:
            if piano_config.current_detect_key_algorithm == 2:
                self.detect_key_info = mp.alg.detect_scale3(
                    self.musicsheet,
                    get_scales=True,
                    most_appear_num=piano_config.
                    current_detect_key_most_appear_num,
                    major_minor_preference=piano_config.
                    current_detect_key_major_minor_preference,
                    unit=piano_config.current_detect_key_unit,
                    key_accuracy_tol=piano_config.
                    current_detect_key_key_accuracy_tol)
                start = start_time * self.unit_time + current_piano_window.bars_drop_interval
                for each in self.detect_key_info:
                    each[1] = ', '.join(
                        [f'{i.start.name} {i.mode}' for i in each[1]])
                    current_start, current_stop = each[0]
                    current_start = start + self.unit_time * current_start
                    current_stop = start + self.unit_time * current_stop
                    each[0] = [current_start, current_stop]
                self.detect_key_info_ind = 0
        self._midi_show_init(self.musicsheet, self.unit_time,
                             self.musicsheet.start_time)
        if piano_config.show_music_analysis:
            self.show_music_analysis_list = [[
                mp.alg.add_to_last_index(self.musicsheet.interval, each[0]),
                each[1]
            ] for each in current_piano_window.music_analysis_list]
            self.default_show_music_analysis_list = copy(
                self.show_music_analysis_list)

        self.startplay = time.time()
        self.finished = False
        self.paused = False
        if piano_config.show_current_detect_key:
            self.current_play_chords = mp.chord([])
            current_piano_window.current_detect_key_label.text = ''
        if piano_config.note_mode != 'bars drop':
            piano_config.show_notes_delay = 0

    def _midi_show_init(self,
                        musicsheet,
                        unit_time,
                        start_time,
                        window_mode=0):
        self.play_midi_file = False
        self.start = start_time * unit_time + current_piano_window.bars_drop_interval
        self._midi_show_init_as_midi(musicsheet, unit_time, start_time,
                                     window_mode)

    def _midi_show_init_as_midi(self, musicsheet, unit_time, start_time,
                                window_mode):
        self.play_midi_file = True
        if window_mode == 0:
            if not self.if_merge:
                mp.write(musicsheet,
                         60 / (unit_time / 4),
                         start_time=musicsheet.start_time,
                         name='temp.mid')
                if piano_config.use_soundfont:
                    current_piano_window.current_sf2_player.current_midi_file = 'temp.mid'
                else:
                    self._load_file('temp.mid')
            else:
                with open(self.path, 'rb') as f:
                    if f.read(4) == b'RIFF':
                        is_riff_midi = True
                    else:
                        is_riff_midi = False
                if not is_riff_midi:
                    if piano_config.use_soundfont:
                        current_piano_window.current_sf2_player.current_midi_file = self.path
                else:
                    current_path = mp.riff_to_midi(self.path)
                    current_buffer = current_path.getbuffer()
                    with open('temp.mid', 'wb') as f:
                        f.write(current_buffer)
                    if piano_config.use_soundfont:
                        current_piano_window.current_sf2_player.current_midi_file = 'temp.mid'
                    else:
                        self._load_file('temp.mid')
        current_start_time = current_piano_window.bars_drop_interval
        if not piano_config.use_soundfont:
            current_start_time -= piano_config.play_midi_start_process_time
            if current_start_time < 0:
                current_start_time = 0
            try:
                self._init_send_midi(current_start_time)
            except Exception as e:
                current_piano_window.label.text = str(e)
                current_piano_window.label.draw()
                current_piano_window.flip()
                pyglet.clock.schedule_once(
                    lambda dt: current_piano_window._go_back_func(), 1)
                time.sleep(1)
                return
        else:
            self.current_position = 0
        self._midi_show_init_note_list(musicsheet, unit_time)
        self.midi_file_play()

    def _init_send_midi(self, current_start_time):
        if piano_config.play_midi_port is not None:
            self.current_output_port_num = piano_config.play_midi_port
        else:
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
            if midi_info:
                midi_output_port = [i[0] for i in midi_info if i[1][2] == 0]
                if not midi_output_port:
                    raise Exception('Error: cannot find any MIDI output port')
                else:
                    self.current_output_port_num = midi_output_port[0]
            else:
                raise Exception('Error: cannot find any MIDI output port')
        self.event_list = control.piece_to_event_list(self.current_piece,
                                                      set_instrument=True)
        for each in self.event_list:
            each.time += current_start_time
        self.current_position = 0
        self.midi_event_length = len(self.event_list)

    def _load_file(self, path):
        self.current_piece = mp.read(path)
        current_start_time = current_piano_window.bars_drop_interval
        current_start_time -= piano_config.play_midi_start_process_time
        if current_start_time < 0:
            current_start_time = 0
        try:
            self._init_send_midi(current_start_time)
        except Exception as e:
            current_piano_window.label.text = str(e)
            current_piano_window.label.draw()
            current_piano_window.flip()
            pyglet.clock.schedule_once(
                lambda dt: current_piano_window._go_back_func(), 1)
            time.sleep(1)
            return

    def _midi_show_init_note_list(self, musicsheet, unit_time):
        self.bars_drop_time.clear()
        musicsheet.clear_pitch_bend('all')
        self.musicsheet = musicsheet
        self.wholenotes = self.musicsheet.notes
        self.sheetlen = len(self.musicsheet)
        self.stop_time = unit_time * (self.start + sum(
            musicsheet.interval[:-1]) + musicsheet.notes[-1].duration)
        if piano_config.note_mode in note_display_mode:
            current_start_time = self.start
            for i in range(self.sheetlen):
                currentnote = musicsheet.notes[i]
                duration = unit_time * currentnote.duration
                interval = unit_time * musicsheet.interval[i]
                currentstart = current_start_time
                if piano_config.note_mode == 'bars drop':
                    current_drop_time = [
                        currentstart - current_piano_window.bars_drop_interval,
                        currentnote, 0
                    ]
                else:
                    current_drop_time = [
                        currentstart + piano_config.bars_mode_delay_time,
                        currentnote, 0
                    ]
                self.bars_drop_time.append(current_drop_time)
                current_start_time += interval

    def mode_self_pc(self, dt):
        self._pc_read_pc_keyboard_special_key()
        self._pc_read_pc_keyboard_key()
        self._pc_read_stillplay_notes()
        if piano_config.note_mode in note_display_mode and piano_config.note_mode:
            self._pc_move_note_bar()
        if self.changed:
            self._pc_update_notes()

    def _pc_read_pc_keyboard_special_key(self):
        if piano_config.config_enable:
            self.detect_config()
        if current_piano_window.keyboard_handler[
                current_piano_window.pause_key]:
            pygame.mixer.stop()
            if piano_config.pause_key_clear_notes:
                if piano_config.delay:
                    self.stillplay = []

    def _pc_read_pc_keyboard_key(self):
        self.current = [
            current_piano_window.map_key_dict_reverse[i]
            for i, j in current_piano_window.keyboard_handler.items()
            if j and i in current_piano_window.map_key_dict_reverse
        ]
        self.current = [i for i in self.current if i in self.wavdic]
        if piano_config.delay:
            self.stillplay_obj = [x[0] for x in self.stillplay]
            self.truecurrent = self.current.copy()
        for each in self.current:
            if piano_config.delay:
                if each in self.stillplay_obj:
                    inds = self.stillplay_obj.index(each)
                    if not self.stillplay[inds][2] and time.time(
                    ) - self.stillplay[inds][1] > piano_config.touch_interval:
                        self.wavdic[each].fadeout(piano_config.fadeout_ms)
                        self.stillplay.pop(inds)
                        self.stillplay_obj.pop(inds)
                else:
                    self.changed = True
                    self.wavdic[each].play()
                    self.stillplay.append([each, time.time(), True])
                    self.stillplay_obj.append(each)
                    if piano_config.note_mode in note_display_mode and piano_config.note_mode:
                        current_bar = self._pc_draw_note_bar(each)
                    else:
                        current_bar = None
                    self._pc_set_piano_key_color(each, current_bar)
            else:
                if each not in self.last:
                    self.changed = True
                    self.wavdic[each].play()
                    if piano_config.note_mode in note_display_mode and piano_config.note_mode:
                        current_bar = self._pc_draw_note_bar(each)
                    else:
                        current_bar = None
                    self._pc_set_piano_key_color(each, current_bar)

    def _pc_draw_note_bar(self, each):
        current_note = mp.to_note(self.notedic[each])
        places = current_piano_window.note_place[current_note.degree - 21]
        current_bar = pyglet.shapes.BorderedRectangle(
            x=places[0] + current_piano_window.bar_offset_x,
            y=current_piano_window.bar_y,
            width=current_piano_window.bar_width,
            height=current_piano_window.bar_height,
            color=piano_config.bar_color if piano_config.color_mode == 'normal'
            else (random.randint(0, 255), random.randint(0, 255),
                  random.randint(0, 255)),
            batch=current_piano_window.batch,
            group=current_piano_window.play_highlight,
            border=piano_config.bar_border,
            border_color=piano_config.bar_border_color)
        current_bar.opacity = piano_config.bar_opacity
        self.still_hold_pc.append([each, current_bar])
        return current_bar

    def _pc_set_piano_key_color(self, each, current_bar=None):
        current_note = mp.to_note(self.notedic[each])
        current_piano_key = current_piano_window.piano_keys[current_note.degree
                                                            - 21]
        if piano_config.color_mode == 'normal':
            current_piano_key.color = piano_config.bar_color
        else:
            if piano_config.note_mode in note_display_mode:
                current_piano_key.color = current_bar.color
            else:
                current_piano_key.color = (random.randint(0, 255),
                                           random.randint(0, 255),
                                           random.randint(0, 255))
        current_piano_key.current_color = current_piano_key.color

    def _pc_read_stillplay_notes(self):
        for j in self.last:
            if j not in self.current:
                if piano_config.delay:
                    if j in self.stillplay_obj:
                        ind = self.stillplay_obj.index(j)
                        stillobj = self.stillplay[ind]
                        if time.time() - stillobj[1] > piano_config.delay_time:
                            self.changed = True
                            self.wavdic[j].fadeout(piano_config.fadeout_ms)
                            self.stillplay.pop(ind)
                            self.stillplay_obj.pop(ind)
                        else:
                            self.stillplay[ind][2] = False
                            self.current.append(j)
                    else:
                        self.changed = True
                        self.wavdic[j].fadeout(piano_config.fadeout_ms)
                else:
                    self.changed = True
                    self.wavdic[j].fadeout(piano_config.fadeout_ms)
        self.last = self.current

    def _pc_move_note_bar(self):
        i = 0
        while i < len(self.plays):
            each = self.plays[i]
            each.y += current_piano_window.bar_steps
            if each.y >= current_piano_window.height:
                each.batch = None
                del self.plays[i]
                continue
            i += 1
        for k in self.still_hold_pc:
            current_hold_note, current_bar = k
            if current_hold_note in self.truecurrent:
                current_bar.height += current_piano_window.bar_hold_increase
            else:
                self.plays.append(current_bar)
                self.still_hold_pc.remove(k)

    def _pc_clear_all_bars(self):
        for each in self.still_hold_pc:
            each[1].batch = None
        self.still_hold_pc.clear()
        for each in self.plays:
            each.batch = None
        self.plays.clear()

    def _pc_update_notes(self):
        self.changed = False
        if piano_config.delay:
            if piano_config.delay_only_read_current:
                notels = [self.notedic[t] for t in self.truecurrent]
            else:
                notels = [self.notedic[t] for t in self.stillplay_obj]
        else:
            notels = [self.notedic[t] for t in self.last]
        if self.lastshow:
            for t in self.lastshow:
                current_piano_window.piano_keys[
                    t.degree -
                    21].color = current_piano_window.initial_colors[t.degree -
                                                                    21]
        if notels:
            self.currentchord = mp.chord(notels)
            for k in self.currentchord:
                current_piano_key = current_piano_window.piano_keys[k.degree -
                                                                    21]
                current_piano_key.color = piano_config.bar_color if piano_config.color_mode == 'normal' else current_piano_key.current_color
            self.currentchord.notes.sort(key=lambda x: x.degree)
            if self.currentchord != self.lastshow:
                self.lastshow = self.currentchord
                current_piano_window.label.text = self._show_notes(
                    self.currentchord.notes)
                if piano_config.show_chord and any(
                        type(t) == mp.note for t in self.currentchord):
                    chordtype = self._detect_chord(self.currentchord)

                    current_piano_window.label2.text = str(chordtype)
        else:
            self.lastshow = notels
            current_piano_window.label.text = str(notels)
            current_piano_window.label2.text = ''
        if piano_config.show_key:
            current_piano_window.label.text = str(self.truecurrent)

    def _show_notes(self, currentchord):
        if piano_config.show_chord_accidentals == 'flat':
            return str([~i if '#' in i.name else i for i in currentchord])
        else:
            return str(currentchord)

    def mode_self_midi(self, dt):
        self._midi_keyboard_read_stillplay_notes()
        self._midi_keyboard_update_notes()
        self._midi_keyboard_read_device_midi_events()
        self._midi_keyboard_draw_notes()
        self._midi_keyboard_read_pc_keyboard_key()

    def _midi_keyboard_read_stillplay_notes(self):
        self.current_time = time.time()
        for each in self.stillplay:
            if each not in self.current_play:
                if piano_config.delay_only_read_current:
                    if not each.sustain_pedal_on:
                        if self.current_time - each.count_time >= piano_config.delay_time:
                            if piano_config.load_sound:
                                current_note_text = str(each)
                                if current_note_text in self.wavdic:
                                    self.wavdic[current_note_text].fadeout(
                                        piano_config.fadeout_ms)
                            self.stillplay.remove(each)
                    else:
                        current_piano_window.piano_keys[
                            each.degree -
                            21].color = piano_config.sustain_bar_color
                else:
                    current_piano_window.piano_keys[
                        each.degree -
                        21].color = piano_config.sustain_bar_color
            else:
                each.count_time = self.current_time

        if piano_config.delay_only_read_current:
            currentchord = []
            for i in self.current_play + [
                    i for i in self.stillplay if i.sustain_pedal_on
            ]:
                if i not in currentchord:
                    currentchord.append(i)
            if currentchord:
                self.currentchord = mp.chord(currentchord)
                self.currentchord.notes.sort(key=lambda x: x.degree)
                current_piano_window.label.text = self._show_notes(
                    self.currentchord.notes)
                if piano_config.show_chord:
                    if not (self.last_time_currentchord and self.currentchord
                            == self.last_time_currentchord):
                        chordtype = self._detect_chord(self.currentchord)
                        self.last_time_currentchord = self.currentchord
                        self.last_time_chordtype = chordtype
                    else:
                        chordtype = self.last_time_chordtype
                    current_piano_window.label2.text = str(chordtype)
            else:
                current_piano_window.label.text = '[]'
                current_piano_window.label2.text = ''

    def _midi_keyboard_clear_all_bars(self):
        for each in self.still_hold:
            each[1].batch = None
        self.still_hold.clear()
        for each in self.plays:
            each.batch = None
        self.plays.clear()

    def _midi_keyboard_update_notes(self):
        if (not self.sostenuto_pedal_on) and self.last != self.current_play:
            self.last = self.current_play.copy()
            if self.current_play:
                self.currentchord = mp.chord(
                    self.current_play
                ) if piano_config.delay_only_read_current else mp.chord(
                    self.stillplay)
                self.currentchord.notes.sort(key=lambda x: x.degree)
                current_piano_window.label.text = self._show_notes(
                    self.currentchord.notes)
                if piano_config.show_chord and any(
                        type(t) == mp.note for t in self.currentchord):
                    if not (self.last_time_currentchord and self.currentchord
                            == self.last_time_currentchord):
                        chordtype = self._detect_chord(self.currentchord)
                        self.last_time_currentchord = self.currentchord
                        self.last_time_chordtype = chordtype
                    else:
                        chordtype = self.last_time_chordtype

                    current_piano_window.label2.text = str(chordtype)
            else:
                if piano_config.delay_only_read_current:
                    current_piano_window.label.text = '[]'
                    current_piano_window.label2.text = ''

    def _midi_keyboard_read_device_midi_events(self):
        if self.device.poll():
            event = self.device.read(1)[0]
            data, timestamp = event
            status, note_number, velocity, note_off_velocity = data
            if status == 128 or (status == 144 and velocity == 0):
                current_note = mp.degree_to_note(note_number)
                current_note.sustain_pedal_on = False
                # 128 is the status code of note off in midi
                if piano_config.delay_only_read_current:
                    if 0 <= note_number - 21 < current_piano_window.note_num:
                        current_piano_window.piano_keys[
                            note_number -
                            21].color = current_piano_window.initial_colors[
                                note_number - 21]
                if current_note in self.current_play:
                    self.current_play.remove(current_note)
            elif status == 144:
                current_note = mp.degree_to_note(note_number)
                current_note.sustain_pedal_on = False
                # 144 is the status code of note on in midi
                if piano_config.note_mode in note_display_mode and piano_config.note_mode:
                    if 0 <= current_note.degree - 21 < current_piano_window.note_num:
                        places = current_piano_window.note_place[
                            current_note.degree - 21]
                        current_bar = pyglet.shapes.BorderedRectangle(
                            x=places[0] + current_piano_window.bar_offset_x,
                            y=current_piano_window.bar_y,
                            width=current_piano_window.bar_width,
                            height=current_piano_window.bar_height,
                            color=piano_config.bar_color
                            if piano_config.color_mode == 'normal' else
                            (random.randint(0, 255), random.randint(0, 255),
                             random.randint(0, 255)),
                            batch=current_piano_window.batch,
                            group=current_piano_window.play_highlight,
                            border=piano_config.bar_border,
                            border_color=piano_config.bar_border_color)
                        current_bar.opacity = 255 * (
                            velocity / 127
                        ) if piano_config.opacity_change_by_velocity else piano_config.bar_opacity
                        self.still_hold.append([current_note, current_bar])
                if 0 <= current_note.degree - 21 < current_piano_window.note_num:
                    current_piano_key = current_piano_window.piano_keys[
                        current_note.degree - 21]
                    if piano_config.color_mode == 'normal':
                        current_piano_key.color = piano_config.bar_color
                    else:
                        if piano_config.note_mode in note_display_mode:
                            current_piano_key.color = current_bar.color
                        else:
                            current_piano_key.color = (random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255))
                if current_note not in self.current_play:
                    self.current_play.append(current_note)
                    if current_note not in self.stillplay:
                        self.stillplay.append(current_note)
                    current_note.count_time = self.current_time
                    if piano_config.load_sound:
                        current_note_text = str(current_note)
                        if current_note_text in self.wavdic:
                            current_sound = self.wavdic[current_note_text]
                            current_sound.set_volume(
                                self.soft_pedal_volume_ratio * velocity / 127)
                            current_sound.play()
            elif status == 176:
                if note_number == 64:
                    if velocity >= 64:
                        if piano_config.delay_only_read_current:
                            self.stillplay = copy(self.current_play)
                            piano_config.delay_only_read_current = False
                    else:
                        if not piano_config.delay_only_read_current:
                            for each in self.stillplay:
                                pyglet.clock.schedule_once(
                                    self.piano_key_reset,
                                    piano_config.delay_time -
                                    (self.current_time - each.count_time),
                                    each)
                            self.last = copy(self.stillplay)
                            piano_config.delay_only_read_current = True
                elif note_number == 66:
                    if velocity >= 64:
                        if not self.sostenuto_pedal_on:
                            self.sostenuto_pedal_on = True
                            for each in self.current_play:
                                each.sustain_pedal_on = True
                    else:
                        if self.sostenuto_pedal_on:
                            for each in self.stillplay:
                                each.sustain_pedal_on = False
                            for each in self.stillplay:
                                pyglet.clock.schedule_once(
                                    self.piano_key_reset,
                                    piano_config.delay_time -
                                    (self.current_time - each.count_time),
                                    each)
                            self.sostenuto_pedal_on = False
                elif note_number == 67:
                    if velocity >= 64:
                        self.soft_pedal_volume_ratio = piano_config.soft_pedal_volume
                    else:
                        self.soft_pedal_volume_ratio = 1

    def _midi_keyboard_draw_notes(self):
        if piano_config.note_mode in note_display_mode and piano_config.note_mode:
            i = 0
            while i < len(self.plays):
                each = self.plays[i]
                each.y += current_piano_window.bar_steps
                if each.y >= current_piano_window.height:
                    each.batch = None
                    del self.plays[i]
                    continue
                i += 1
            for k in self.still_hold:
                current_hold_note, current_bar = k
                if current_hold_note in self.current_play:
                    current_bar.height += current_piano_window.bar_hold_increase
                else:
                    self.plays.append(current_bar)
                    self.still_hold.remove(k)

    def _midi_keyboard_read_pc_keyboard_key(self):
        if piano_config.config_enable:
            if piano_config.play_use_soundfont:
                self.detect_sf2_config(1)

    def mode_midi_show(self, dt):
        if not self.paused:
            self._midi_show_playing()
        else:
            self._midi_show_pause()
        if self.finished:
            if piano_config.note_mode == 'bars drop' and piano_config.show_notes_delay:
                pyglet.clock.schedule_once(self._midi_show_finished,
                                           piano_config.show_notes_delay)
            else:
                self._midi_show_finished()

    def _midi_show_playing(self):
        self.current_past_time = time.time(
        ) - self.startplay + self.current_position
        self.current_progress_percentage = (
            self.current_past_time -
            piano_config.move_progress_adjust_time) / self.stop_time
        current_progress_bar_length = current_piano_window.progress_bar_length * self.current_progress_percentage
        current_piano_window.current_progress_bar.width = current_progress_bar_length + 2
        if piano_config.note_mode == 'bars drop':
            self._midi_show_draw_notes_bars_drop_mode()
            self._midi_show_draw_notes_hit_key_bars_drop_mode()
        elif piano_config.note_mode == 'bars':
            self._midi_show_draw_notes_bars_mode()
            self._midi_show_draw_notes_hit_key_bars_mode()
        elif piano_config.note_mode == '':
            self._midi_show_draw_notes_bars_mode(mode=1)
            self._midi_show_draw_notes_hit_key_bars_mode()
        if self.current_past_time >= self.stop_time:
            self.finished = True

    def _midi_show_draw_notes_bars_drop_mode(self):
        if self.bars_drop_time:
            for i, next_bar_drop in enumerate(self.bars_drop_time):
                current_bars_drop_start_time, current_note, status = next_bar_drop
                if status == 0 and self.current_past_time >= current_bars_drop_start_time:
                    places = current_piano_window.note_place[
                        current_note.degree - 21]
                    current_bar = pyglet.shapes.BorderedRectangle(
                        x=places[0] + current_piano_window.bar_offset_x,
                        y=current_piano_window.height,
                        width=current_piano_window.bar_width,
                        height=current_piano_window.bar_unit *
                        current_note.duration / (self.bpm / 130),
                        color=current_note.own_color
                        if piano_config.use_track_colors else
                        (piano_config.bar_color
                         if piano_config.color_mode == 'normal' else
                         (random.randint(0, 255), random.randint(0, 255),
                          random.randint(0, 255))),
                        batch=current_piano_window.batch,
                        group=current_piano_window.bottom_group,
                        border=piano_config.bar_border,
                        border_color=piano_config.bar_border_color)
                    current_bar.opacity = 255 * (
                        current_note.volume / 127
                    ) if piano_config.opacity_change_by_velocity else piano_config.bar_opacity
                    current_bar.num = current_note.degree - 21
                    current_bar.hit_key = False
                    current_bar.current_note = current_note
                    current_bar.ind = i
                    self.plays.append(current_bar)
                    next_bar_drop[2] = 1

    def _midi_show_draw_notes_bars_mode(self, mode=0):
        if self.bars_drop_time:
            changed = False
            for i, next_bar_drop in enumerate(self.bars_drop_time):
                current_bars_drop_start_time, current_note, status = next_bar_drop
                if status == 0 and self.current_past_time >= current_bars_drop_start_time:
                    places = current_piano_window.note_place[
                        current_note.degree - 21]
                    current_height = current_piano_window.bar_unit * current_note.duration / (
                        self.bpm / 130)
                    current_bar = pyglet.shapes.BorderedRectangle(
                        x=places[0] + current_piano_window.bar_offset_x,
                        y=current_piano_window.bar_y - current_height,
                        width=current_piano_window.bar_width,
                        height=current_height,
                        color=current_note.own_color
                        if piano_config.use_track_colors else
                        (piano_config.bar_color
                         if piano_config.color_mode == 'normal' else
                         (random.randint(0, 255), random.randint(0, 255),
                          random.randint(0, 255))),
                        batch=current_piano_window.batch,
                        group=current_piano_window.bottom_group,
                        border=piano_config.bar_border,
                        border_color=piano_config.bar_border_color)
                    if mode == 1:
                        current_bar.opacity = 0
                    else:
                        current_bar.opacity = 255 * (
                            current_note.volume / 127
                        ) if piano_config.opacity_change_by_velocity else piano_config.bar_opacity
                    current_bar.num = current_note.degree - 21
                    current_bar.hit_key = False
                    current_bar.current_note = current_note
                    current_bar.ind = i
                    self.plays.append(current_bar)
                    current_piano_window.piano_keys[
                        current_note.degree - 21].color = current_bar.color
                    next_bar_drop[2] = 1
                    self.current_hit_key_notes.append(current_note)
                    changed = True

                    if piano_config.show_music_analysis:
                        if self.show_music_analysis_list:
                            for current_music_analysis in self.show_music_analysis_list:
                                if i == current_music_analysis[0]:
                                    current_piano_window.music_analysis_label.text = current_music_analysis[
                                        1]
                                    break
            if changed:
                self._midi_show_update_notes()

    def _midi_show_update_notes(self):
        if self.current_hit_key_notes:
            self.current_hit_key_notes.sort(key=lambda x: x.degree)
            if not piano_config.show_notes_delay:
                self._midi_show_update_notes_text(
                    playnotes=self.current_hit_key_notes)
            else:
                pyglet.clock.schedule_once(
                    self._midi_show_update_notes_text,
                    piano_config.show_notes_delay,
                    playnotes=self.current_hit_key_notes)

    def _midi_show_update_notes_text(self, dt=None, playnotes=None):
        if piano_config.show_notes:
            current_piano_window.label.text = self._show_notes(playnotes)
        if piano_config.show_chord and any(
                type(t) == mp.note for t in playnotes):
            chordtype = self._detect_chord(playnotes)
            current_piano_window.label2.text = str(chordtype)

    def _midi_show_playing_read_pc_keyboard_key(self, dt):
        if current_piano_window.keyboard_handler[
                current_piano_window.pause_key]:
            if self.play_midi_file:
                if piano_config.use_soundfont:
                    if current_piano_window.current_sf2_player.playing:
                        current_piano_window.current_sf2_player.pause()
                        self.paused = True
                else:
                    self.current_send_midi_queue.put('pause')
                    self.paused = True
            else:
                self.paused = True
            if self.paused:
                self.pause_start = time.time()
                current_piano_window.message_label = True
                current_piano_window.label3.text = language_patch.ideal_piano_language_dict[
                    'pause'].format(unpause_key=piano_config.unpause_key)

    def _midi_show_playing_read_pc_move_progress_key(self, dt):
        if self.finished:
            return
        if current_piano_window.keyboard_handler[
                current_piano_window.map_key_dict[
                    piano_config.move_progress_left_key]]:
            self._midi_show_set_position(self.current_past_time -
                                         piano_config.move_progress_left_unit)
        elif current_piano_window.keyboard_handler[
                current_piano_window.map_key_dict[
                    piano_config.move_progress_right_key]]:
            self._midi_show_set_position(self.current_past_time +
                                         piano_config.move_progress_right_unit)

    def _midi_show_set_position(self, position):
        if piano_config.use_soundfont:
            if not current_piano_window.current_sf2_player.playing:
                return
            current_use_soundfont_delay_time = piano_config.use_soundfont_delay_time if piano_config.note_mode == 'bars drop' else 0
            current_sf2_time = position - piano_config.bars_drop_interval + piano_config.move_progress_adjust_time - current_use_soundfont_delay_time
            if current_sf2_time < 0:
                position += abs(current_sf2_time)
                current_sf2_time = 0
        self.current_position = position
        if self.current_position < 0:
            self.current_position = 0
        if self.current_position >= self.stop_time:
            self.current_position = self.stop_time
        self.startplay = time.time() - piano_config.move_progress_adjust_time
        if piano_config.note_mode in note_display_mode:
            current_past_time = time.time(
            ) - self.startplay + self.current_position
            for each in self.bars_drop_time:
                if each[2] == 1 and each[0] >= current_past_time:
                    each[2] = 0
                elif each[2] == 0 and each[0] < current_past_time:
                    each[2] = 1

        if not piano_config.use_soundfont:
            self.current_send_midi_queue.put(
                ['set_position', self.current_position])
        else:
            current_sf2_player = current_piano_window.current_sf2_player
            current_ticks = int(
                mp.mido.second2tick(current_sf2_time,
                                    self.current_ticks_per_beat,
                                    current_sf2_player.get_current_tempo()))
            current_sf2_player.set_pos(current_ticks)
        self._midi_show_clear_all_bars_drop()

    def _midi_show_clear_all_bars_drop(self):
        for each in self.plays:
            each.batch = None
            current_piano_window.piano_keys[
                each.num].color = current_piano_window.initial_colors[each.num]
        self.plays.clear()
        if piano_config.show_notes:
            current_piano_window.label.text = ''
        if piano_config.show_chord:
            current_piano_window.label2.text = ''
        self.current_hit_key_notes.clear()

    def _midi_show_draw_notes_hit_key_bars_mode(self):
        changed = False
        i = 0
        while i < len(self.plays):
            each = self.plays[i]
            each.y += current_piano_window.drop_bar_steps
            if not each.hit_key and each.y >= current_piano_window.bar_y:
                each.hit_key = True
                current_piano_window.piano_keys[
                    each.num].color = current_piano_window.initial_colors[
                        each.num]
                self.current_hit_key_notes.remove(each.current_note)
                changed = True
            if each.y >= current_piano_window.height:
                each.batch = None
                del self.plays[i]
                continue
            i += 1
        if changed:
            self._midi_show_update_notes()

    def _midi_show_draw_notes_hit_key_bars_drop_mode(self):
        changed = False
        i = 0
        while i < len(self.plays):
            each = self.plays[i]
            each.y -= current_piano_window.drop_bar_steps
            if not each.hit_key and each.y <= current_piano_window.bars_drop_place:
                each.hit_key = True
                self.current_hit_key_notes.append(each.current_note)
                current_piano_window.piano_keys[each.num].color = each.color
                changed = True

                if piano_config.show_music_analysis:
                    if self.show_music_analysis_list:
                        for current_music_analysis in self.show_music_analysis_list:
                            if each.ind == current_music_analysis[0]:
                                current_piano_window.music_analysis_label.text = current_music_analysis[
                                    1]
                                break

            if each.height + each.y <= current_piano_window.piano_height:
                each.batch = None
                current_piano_window.piano_keys[
                    each.num].color = current_piano_window.initial_colors[
                        each.num]
                del self.plays[i]
                self.current_hit_key_notes.remove(each.current_note)
                changed = True
                continue
            i += 1
        if changed:
            self._midi_show_update_notes()

    def _midi_show_pause(self):
        if current_piano_window.keyboard_handler[
                current_piano_window.unpause_key]:
            if self.play_midi_file:
                if piano_config.use_soundfont:
                    current_piano_window.current_sf2_player.unpause()
                else:
                    self.current_send_midi_queue.put('unpause')
            self.paused = False
            current_piano_window.message_label = False
            pause_stop = time.time()
            pause_time = pause_stop - self.pause_start
            self.startplay += pause_time

    def _midi_show_finished(self, dt=None):
        if piano_config.note_mode != 'bars drop':
            if self.current_hit_key_notes:
                for t in self.current_hit_key_notes:
                    current_piano_window.piano_keys[
                        t.degree -
                        21].color = current_piano_window.initial_colors[
                            t.degree - 21]
        current_piano_window.label2.text = ''
        for each in self.plays:
            each.batch = None
        if piano_config.show_music_analysis:
            current_piano_window.music_analysis_label.text = ''
            self.show_music_analysis_list = copy(
                self.default_show_music_analysis_list)
        current_piano_window.label.text = language_patch.ideal_piano_language_dict[
            'repeat'].format(repeat_key=piano_config.repeat_key)
        if current_piano_window.keyboard_handler[
                current_piano_window.repeat_key]:
            if piano_config.note_mode in note_display_mode:
                self.plays.clear()
                pyglet.clock.unschedule(self._midi_show_update_notes_text)
                pyglet.clock.unschedule(self._midi_show_finished)
            for k in range(len(current_piano_window.piano_keys)):
                current_piano_window.piano_keys[
                    k].color = current_piano_window.initial_colors[k]
            current_piano_window.label.text = ''
            current_piano_window.redraw()
            self._midi_show_init(self.musicsheet,
                                 self.unit_time,
                                 self.musicsheet.start_time,
                                 window_mode=1)
            self.startplay = time.time()
            self.current_hit_key_notes.clear()
            current_piano_window.current_progress_bar.width = 2
            self.finished = False
            if piano_config.show_current_detect_key:
                self.current_play_chords = mp.chord([])
                current_piano_window.current_detect_key_label.text = ''
                self.detect_key_info_ind = 0


if __name__ == '__main__':
    multiprocessing.freeze_support()
    current_piano_engine = piano_engine()
    current_piano_window = piano_window()
    pyglet.clock.schedule_interval(update, 1 / piano_config.fps)
    pyglet.app.run()
