import random

if sys.platform == 'darwin':
    current_test = tk.Tk()
    current_test.withdraw()
    current_test.destroy()

if piano_config.language == 'English':
    from languages.en import language_patch
elif piano_config.language == 'Chinese':
    from languages.cn import language_patch
    mp.detect = language_patch.detect

if (piano_config.play_as_midi
        and piano_config.use_soundfont) or piano_config.play_use_soundfont:
    import sf2_loader as rs

key = pyglet.window.key


def get_off_sort(a):
    identifier = language_patch.ideal_piano_language_dict['sort']
    each_chord = a.split('/')
    for i in range(len(each_chord)):
        current = each_chord[i]
        if identifier in current:
            current = current[:current.index(identifier) - 1]
            if current[0] == '[':
                current += ']'
            each_chord[i] = current
    return '/'.join(each_chord)


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}/{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


def load_sf2(dic, sf2, volume):
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
    return wavedict


def get_image(img):
    return pyglet.image.load(img).get_texture()


def update(dt):
    pass


class ideal_piano_button:
    def __init__(self, img, x, y):
        self.img = get_image(img).get_transform()
        self.img.width /= piano_config.button_resize_num
        self.img.height /= piano_config.button_resize_num
        self.x = x
        self.y = y
        self.button = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
        self.ranges = [self.x, self.x + self.img.width
                       ], [self.y, self.y + self.img.height]

    def get_range(self):
        height, width = self.img.height, self.img.width
        return [self.x, self.x + width], [self.y, self.y + height]

    def inside(self, mouse_pos):
        range_x, range_y = self.ranges
        return range_x[0] <= mouse_pos[0] <= range_x[1] and range_y[
            0] <= mouse_pos[1] <= range_y[1]

    def draw(self):
        self.button.draw()


class piano_window(pyglet.window.Window):
    def __init__(self):
        self.init_window()
        self.init_parameters()
        self.init_key_map()
        self.init_keys()
        self.init_sf2()
        self.init_screen()
        self.init_layers()
        self.init_screen_buttons()
        self.init_piano_keys()
        self.init_note_mode()
        self.init_screen_labels()
        self.init_music_analysis()

    def init_window(self):
        super(piano_window, self).__init__(*piano_config.screen_size,
                                           caption='Ideal Piano',
                                           resizable=True)
        self.icon = pyglet.image.load('resources/piano.ico')
        self.set_icon(self.icon)
        self.keyboard_handler = key.KeyStateHandler()
        self.push_handlers(self.keyboard_handler)

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
        else:
            if piano_config.play_use_soundfont or (
                    piano_config.play_as_midi and piano_config.use_soundfont):
                if 'rs' not in sys.modules:
                    global rs
                    import sf2_loader as rs
        if piano_config.play_use_soundfont or (
                piano_config.play_as_midi and piano_config.use_soundfont
                and piano_config.render_as_audio):
            self.current_sf2 = rs.sf2_loader(piano_config.sf2_path)
            self.current_sf2.change(bank=piano_config.bank,
                                    preset=piano_config.preset)
        if piano_config.play_as_midi and piano_config.use_soundfont:
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
        self.show_delay_time = int(piano_config.show_delay_time * 1000)
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
            background.width, background.height = piano_config.background_size
        self.background = background

    def init_layers(self):
        self.batch = pyglet.graphics.Batch()
        self.bottom_group = pyglet.graphics.OrderedGroup(0)
        self.piano_bg = pyglet.graphics.OrderedGroup(1)
        self.piano_key = pyglet.graphics.OrderedGroup(2)
        self.play_highlight = pyglet.graphics.OrderedGroup(3)

    def init_note_mode(self):
        if not piano_config.draw_piano_keys:
            self.bar_offset_x = 9
            image = get_image(piano_config.piano_image)
            if not piano_config.piano_size:
                ratio = self.screen_width / image.width
                image.width = self.screen_width
                image.height *= ratio
            else:
                image.width, image.height = piano_config.piano_size
            self.image_show = pyglet.sprite.Sprite(image,
                                                   x=0,
                                                   y=0,
                                                   batch=self.batch,
                                                   group=self.piano_bg)

        current_piano_engine.plays = []
        if piano_config.note_mode == 'bars drop':
            current_piano_engine.bars_drop_time = []
            distances = self.screen_height - self.piano_height
            self.bars_drop_interval = piano_config.bars_drop_interval
            self.bar_steps = (distances / self.bars_drop_interval
                              ) / piano_config.adjust_ratio
        else:
            self.bar_steps = piano_config.bar_steps
            self.bars_drop_interval = 0

    def init_screen_buttons(self):
        if piano_config.language == 'Chinese':
            piano_config.go_back_image = 'packages/languages/cn/go_back.png'
            piano_config.self_play_image = 'packages/languages/cn/play.png'
            piano_config.self_midi_image = 'packages/languages/cn/midi_keyboard.png'
            piano_config.play_midi_image = 'packages/languages/cn/play_midi.png'
        self.go_back_button = ideal_piano_button(piano_config.go_back_image,
                                                 *piano_config.go_back_place)
        self.self_play_button = ideal_piano_button(
            piano_config.self_play_image, *piano_config.self_play_place)
        self.self_midi_button = ideal_piano_button(
            piano_config.self_midi_image, *piano_config.self_midi_place)
        self.play_midi_button = ideal_piano_button(
            piano_config.play_midi_image, *piano_config.play_midi_place)

    def init_screen_labels(self):
        self.label = pyglet.text.Label('',
                                       font_name=piano_config.fonts,
                                       font_size=piano_config.fonts_size,
                                       bold=piano_config.bold,
                                       x=piano_config.label1_place[0],
                                       y=piano_config.label1_place[1],
                                       color=piano_config.message_color,
                                       anchor_x=piano_config.label_anchor_x,
                                       anchor_y=piano_config.label_anchor_y,
                                       multiline=True,
                                       width=1000)
        self.label2 = pyglet.text.Label('',
                                        font_name=piano_config.fonts,
                                        font_size=piano_config.fonts_size,
                                        bold=piano_config.bold,
                                        x=piano_config.label2_place[0],
                                        y=piano_config.label2_place[1],
                                        color=piano_config.message_color,
                                        anchor_x=piano_config.label_anchor_x,
                                        anchor_y=piano_config.label_anchor_y)
        self.label3 = pyglet.text.Label('',
                                        font_name=piano_config.fonts,
                                        font_size=piano_config.fonts_size,
                                        bold=piano_config.bold,
                                        x=piano_config.label3_place[0],
                                        y=piano_config.label3_place[1],
                                        color=piano_config.message_color,
                                        anchor_x=piano_config.label_anchor_x,
                                        anchor_y=piano_config.label_anchor_y)

        self.label_midi_device = pyglet.text.Label(
            '',
            font_name=piano_config.fonts,
            font_size=15,
            bold=piano_config.bold,
            x=250,
            y=400,
            color=piano_config.message_color,
            anchor_x=piano_config.label_anchor_x,
            anchor_y=piano_config.label_anchor_y,
            multiline=True,
            width=1000)

    def init_music_analysis(self):
        if piano_config.show_music_analysis:
            self.music_analysis_label = pyglet.text.Label(
                '',
                font_name=piano_config.fonts,
                font_size=piano_config.music_analysis_fonts_size,
                bold=piano_config.bold,
                x=piano_config.music_analysis_place[0],
                y=piano_config.music_analysis_place[1],
                color=piano_config.message_color,
                anchor_x=piano_config.label_anchor_x,
                anchor_y=piano_config.label_anchor_y,
                multiline=True,
                width=piano_config.music_analysis_width)
            if piano_config.music_analysis_file:
                with open(piano_config.music_analysis_file,
                          encoding='utf-8-sig') as f:
                    data = f.read()
                    lines = [i for i in data.split('\n\n') if i]
                    self.music_analysis_list = []
                    self.current_key = None
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
                                if self.current_key:
                                    current_chords = f'{piano_config.key_header}{self.current_key}\n' + current_chords
                                self.music_analysis_list.append(
                                    [bar_counter, current_chords])
                            else:
                                self.current_key = each.split('key: ')[1]

    def init_piano_keys(self):
        self.piano_height = piano_config.white_key_y + piano_config.white_key_height
        self.piano_keys = []
        self.initial_colors = []
        if piano_config.draw_piano_keys:
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
                    self.piano_keys.append(current_piano_key)
                    self.initial_colors.append(
                        (current_start, piano_config.black_key_color))
                current_start += piano_config.black_keys_set_interval
            self.piano_keys.sort(key=lambda s: s.x)
            self.initial_colors.sort(key=lambda s: s[0])
            self.initial_colors = [t[1] for t in self.initial_colors]
            self.note_place = [(each.x, each.y) for each in self.piano_keys]
            self.bar_offset_x = 0

    def init_parameters(self):
        self.mouse_left = 1
        self.mouse_pos = 0, 0
        self.first_time = True
        self.message_label = False
        self.is_click = False
        self.mode_num = None
        self.func = None
        self.click_mode = None
        self.bar_offset_x = piano_config.bar_offset_x
        self.open_browse_window = False

    def init_language(self):
        global language_patch
        if piano_config.language == 'English':
            from languages.en import language_patch
            importlib.reload(mp)
        elif piano_config.language == 'Chinese':
            from languages.cn import language_patch
            mp.detect = language_patch.detect
        current_piano_engine.current_midi_device = language_patch.ideal_piano_language_dict[
            'current_midi_device']

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = x, y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.go_back_button.inside(
                self.mouse_pos
        ) & button & self.mouse_left and not self.first_time:
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
                    pyglet.clock.unschedule(
                        current_piano_engine.midi_file_play)
                    if piano_config.show_music_analysis:
                        self.music_analysis_label.text = ''
                    if piano_config.play_as_midi:
                        if piano_config.use_soundfont and not piano_config.render_as_audio:
                            if self.current_sf2_player.playing:
                                self.current_sf2_player.stop()
                    if current_piano_engine.playls:
                        current_piano_engine.playls.clear()
            self.is_click = True
            self.click_mode = None
            if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                current_piano_engine.still_hold.clear()
                if piano_config.note_mode == 'bars drop':
                    current_piano_engine.bars_drop_time.clear()
            if piano_config.draw_piano_keys:
                for k in range(len(self.piano_keys)):
                    self.piano_keys[k].color = self.initial_colors[k]
            self.label3.text = ''

        if self.self_play_button.inside(
                self.mouse_pos) & button & self.mouse_left and self.first_time:
            self.click_mode = 0
        if self.self_midi_button.inside(
                self.mouse_pos) & button & self.mouse_left and self.first_time:
            self.click_mode = 1
        if self.play_midi_button.inside(
                self.mouse_pos) & button & self.mouse_left and self.first_time:
            self.click_mode = 2

    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        if not piano_config.draw_piano_keys:
            self.image_show.draw()
        if self.batch:
            self.batch.draw()
        self.go_back_button.draw()
        self.label_midi_device.draw()
        if self.first_time:
            self._draw_window_first_time()
        else:
            self._draw_window()

    def _draw_window_first_time(self):
        self.self_play_button.draw()
        self.self_midi_button.draw()
        self.play_midi_button.draw()
        if self.mode_num is None:
            self._main_window_read_click_mode()
        else:
            self._main_window_enter_mode()

    def _main_window_read_click_mode(self):
        if self.keyboard_handler[key.LSHIFT]:
            self.label_midi_device.text = current_piano_engine.current_midi_device
        if self.keyboard_handler[key.LCTRL]:
            self.label_midi_device.text = ''
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
            current_piano_engine.init_self_pc()
            self.label.text = language_patch.ideal_piano_language_dict[
                'finished']
            self.label.draw()
            self.func = current_piano_engine.mode_self_pc
            self.not_first()
            pyglet.clock.schedule_interval(self.func, 1 / piano_config.fps)
        elif self.mode_num == 1:
            try:
                current_piano_engine.init_self_midi()
                if not current_piano_engine.device:
                    self.label.text = language_patch.ideal_piano_language_dict[
                        'no MIDI input']
                    self.mode_num = 3
                    self.reset_click_mode()
                    self.label.draw()
                else:
                    self.label.text = language_patch.ideal_piano_language_dict[
                        'finished']
                    self.label.draw()
                    self.func = current_piano_engine.mode_self_midi
                    self.not_first()
                    pyglet.clock.schedule_interval(self.func,
                                                   1 / piano_config.fps)
            except Exception as e:
                current_piano_engine.has_load(False)
                pygame.midi.quit()
                current_piano_engine.current_midi_device += f'\n{language_patch.ideal_piano_language_dict["error message"]}: {e}'
                self.label.text = language_patch.ideal_piano_language_dict[
                    'no MIDI input']
                self.mode_num = 3
                self.reset_click_mode()
                self.label.draw()
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
        elif self.mode_num == 3:
            time.sleep(1)
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
        if self.message_label:
            self.label3.draw()
        if piano_config.show_music_analysis:
            self.music_analysis_label.draw()

    def redraw(self):
        self.clear()
        self.background.blit(0, 0)
        if not piano_config.draw_piano_keys:
            self.image_show.draw()
        if self.batch:
            self.batch.draw()
        self.go_back_button.draw()
        self.label_midi_device.draw()
        self.label2.draw()
        if self.message_label:
            self.label3.draw()
        if piano_config.show_music_analysis:
            self.music_analysis_label.draw()

    def reset_click_mode(self):
        self.click_mode = None

    def not_first(self):
        self.first_time = not self.first_time

    def open_settings(self):
        self.keyboard_handler[self.config_key] = False
        self.keyboard_handler[key.S] = False
        os.chdir(abs_path)
        current_config_window = config_window()
        current_config_window.mainloop()
        self.reload_settings()

    def reload_settings(self):
        importlib.reload(piano_config)
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


class piano_engine:
    def __init__(self):
        self.init_parameters()

    def init_parameters(self):
        self.notedic = piano_config.key_settings
        self.currentchord = mp.chord([])
        self.playnotes = []
        self.still_hold_pc = []
        self.still_hold = []
        self.paused = False
        self.pause_start = 0
        self.playls = []
        self.bars_drop_time = []
        self.plays = []
        self.midi_device_load = False
        self.current_midi_device = language_patch.ideal_piano_language_dict[
            'current_midi_device']
        self.device = None
        self.play_midi_file = False
        self.sostenuto_pedal_on = False
        self.soft_pedal_volume_ratio = 1

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

    def midi_file_play(self, dt):
        if piano_config.use_soundfont:
            if piano_config.render_as_audio:
                self.current_midi_audio.play()
            else:
                current_piano_window.current_sf2_player.play_midi_file(
                    current_piano_window.current_sf2_player.current_midi_file)
        else:
            pygame.mixer.music.play()

    def piano_key_reset(self, dt, each):
        current_piano_window.piano_keys[
            each.degree -
            21].color = current_piano_window.initial_colors[each.degree - 21]

    def _detect_chord(self, current_chord):
        return mp.detect(
            current_chord, piano_config.detect_mode, piano_config.inv_num,
            piano_config.rootpitch, piano_config.change_from_first,
            piano_config.original_first, piano_config.same_note_special,
            piano_config.whole_detect, piano_config.return_fromchord,
            piano_config.two_show_interval, piano_config.poly_chord_first,
            piano_config.root_position_return_first,
            piano_config.alter_notes_show_degree)

    def init_self_pc(self):
        if not piano_config.play_use_soundfont:
            self.wavdic = load(self.notedic, piano_config.sound_path,
                               piano_config.sound_format,
                               piano_config.global_volume)
        else:
            self.wavdic = load_sf2(self.notedic,
                                   current_piano_window.current_sf2,
                                   piano_config.global_volume)
        self.last = []
        self.changed = False
        if piano_config.delay:
            self.stillplay = []
        self.lastshow = None

    def init_self_midi(self):
        if not self.midi_device_load:
            self.device = None
            self.has_load(True)
            self.current_midi_device = language_patch.ideal_piano_language_dict[
                'close']
            pygame.midi.init()
            midi_info = [(language_patch.ideal_piano_language_dict['default'],
                          pygame.midi.get_default_input_id())]
            midi_info += [(i, pygame.midi.get_device_info(i))
                          for i in range(piano_config.device_info_num)]
            self.current_midi_device += '\n'.join([str(j) for j in midi_info])
            self.device = pygame.midi.Input(piano_config.midi_device_id)
        else:
            if self.device:
                self.device.close()
                pygame.midi.quit()
                pygame.midi.init()
                self.device = pygame.midi.Input(piano_config.midi_device_id)
        notenames = os.listdir(piano_config.sound_path)
        notenames = [x[:x.index('.')] for x in notenames]
        if piano_config.load_sound:
            if not piano_config.play_use_soundfont:
                self.wavdic = load({i: i
                                    for i in notenames},
                                   piano_config.sound_path,
                                   piano_config.sound_format,
                                   piano_config.global_volume)
            else:
                self.wavdic = load_sf2({i: i
                                        for i in notenames},
                                       current_piano_window.current_sf2,
                                       piano_config.global_volume)
        self.current_play = []
        self.stillplay = []
        self.last = self.current_play.copy()
        self.sostenuto_pedal_on = False
        self.soft_pedal_volume_ratio = 1

    def init_midi_show(self):
        current_piano_window.open_browse_window = True
        current_setup = browse.setup(language_patch.browse_language_dict)
        current_piano_window.open_browse_window = False
        self.path = current_setup.file_path
        self.action = current_setup.action
        read_result = current_setup.read_result
        self.sheetlen = current_setup.sheetlen
        set_bpm = current_setup.set_bpm
        self.off_melody = current_setup.off_melody
        self.if_merge = current_setup.if_merge
        play_interval = current_setup.interval
        if self.action == 1:
            self.action = 0
            return 'back'
        if self.path and read_result:
            if read_result != 'error':
                self.bpm, self.musicsheet, start_time = read_result
                self.musicsheet, new_start_time = self.musicsheet.pitch_filter(
                    *piano_config.pitch_range)
                start_time += new_start_time
                self.sheetlen = len(self.musicsheet)
                if set_bpm:
                    self.bpm = float(set_bpm)
            else:
                return 'back'
        else:
            return 'back'

        if self.off_melody:
            self.musicsheet = mp.split_chord(
                self.musicsheet, 'hold', piano_config.melody_tol,
                piano_config.chord_tol, piano_config.get_off_overlap_notes,
                piano_config.average_degree_length,
                piano_config.melody_degree_tol)
            self.sheetlen = len(self.musicsheet)
        if play_interval is not None:
            play_start, play_stop = int(
                self.sheetlen * (play_interval[0] / 100)), int(
                    self.sheetlen * (play_interval[1] / 100))
            if play_start == 0:
                play_start = 1
            self.musicsheet = self.musicsheet[play_start:play_stop + 1]
            self.sheetlen = play_stop + 1 - play_start
        if self.sheetlen == 0:
            return 'back'
        pygame.mixer.set_num_channels(self.sheetlen)
        self.wholenotes = self.musicsheet.notes
        self.unit_time = 4 * 60 / self.bpm

        # every object in playls has a situation flag at the index of 3,
        # 0 means has not been played yet, 1 means it has started playing,
        # 2 means it has stopped playing
        self.musicsheet.start_time = start_time
        self.playls = self._midi_show_init(self.musicsheet, self.unit_time,
                                           start_time)
        if piano_config.show_music_analysis:
            self.show_music_analysis_list = [[
                mp.add_to_last_index(self.musicsheet.interval, each[0]),
                each[1]
            ] for each in current_piano_window.music_analysis_list]
            self.default_show_music_analysis_list = copy(
                self.show_music_analysis_list)
        self.startplay = time.time()
        self.lastshow = None
        self.finished = False
        self.paused = False

    def _midi_show_init(self,
                        musicsheet,
                        unit_time,
                        start_time,
                        window_mode=0):
        self.play_midi_file = False
        playls = []
        self.start = start_time * unit_time + current_piano_window.bars_drop_interval
        if piano_config.play_as_midi:
            self._midi_show_init_as_midi(musicsheet, unit_time, start_time,
                                         playls, window_mode)
        else:
            self._midi_show_init_as_audio(musicsheet, unit_time, start_time,
                                          playls, window_mode)
        return playls

    def _midi_show_init_as_midi(self, musicsheet, unit_time, start_time,
                                playls, window_mode):
        self.play_midi_file = True
        if window_mode == 0:
            if piano_config.use_soundfont and piano_config.render_as_audio:
                current_piano_window.label.text = language_patch.ideal_piano_language_dict[
                    'soundfont']
                current_piano_window.label.draw()
                current_piano_window.flip()
            if not self.if_merge:
                mp.write(musicsheet,
                         60 / (unit_time / 4),
                         start_time=musicsheet.start_time,
                         name='temp.mid')
                if piano_config.use_soundfont:
                    if piano_config.render_as_audio:
                        current_waveform = current_piano_window.current_sf2.export_midi_file(
                            'temp.mid', get_audio=True).raw_data
                        self.current_midi_audio = pygame.mixer.Sound(
                            buffer=current_waveform)
                    else:
                        current_piano_window.current_sf2_player.current_midi_file = 'temp.mid'
                else:
                    pygame.mixer.music.load('temp.mid')
            else:
                try:
                    if piano_config.use_soundfont:
                        if piano_config.render_as_audio:
                            current_waveform = current_piano_window.current_sf2.export_midi_file(
                                self.path, get_audio=True).raw_data
                            self.current_midi_audio = pygame.mixer.Sound(
                                buffer=current_waveform)
                        else:
                            pygame.mixer.music.load(self.path)
                            pygame.mixer.music.unload()
                            current_piano_window.current_sf2_player.current_midi_file = self.path
                    else:
                        pygame.mixer.music.load(self.path)
                except:
                    current_path = mp.riff_to_midi(self.path)
                    current_buffer = current_path.getbuffer()
                    with open('temp.mid', 'wb') as f:
                        f.write(current_buffer)
                    if piano_config.use_soundfont:
                        if piano_config.render_as_audio:
                            current_waveform = current_piano_window.current_sf2.export_midi_file(
                                'temp.mid', get_audio=True).raw_data
                            self.current_midi_audio = pygame.mixer.Sound(
                                buffer=current_waveform)
                        else:
                            current_piano_window.current_sf2_player.current_midi_file = 'temp.mid'
                    else:
                        pygame.mixer.music.load('temp.mid')
        if piano_config.use_soundfont and piano_config.render_as_audio:
            current_piano_window.label.text = ''
            current_piano_window.label.draw()
            current_piano_window.flip()
        pyglet.clock.schedule_once(self.midi_file_play,
                                   current_piano_window.bars_drop_interval)
        self._midi_show_init_note_list(musicsheet, unit_time, playls)

    def _midi_show_init_as_audio(self, musicsheet, unit_time, start_time,
                                 playls, window_mode):
        current_piano_window.label.text = language_patch.ideal_piano_language_dict[
            'sample']
        current_piano_window.label.draw()
        current_piano_window.flip()
        try:
            self._midi_show_init_note_list(musicsheet, unit_time, playls, 1)
        except:
            pygame.mixer.music.load(self.path)
            self.play_midi_file = True
            playls.clear()
            if piano_config.note_mode == 'bars drop':
                self.bars_drop_time.clear()
            self.start = start_time * unit_time + current_piano_window.bars_drop_interval
            self._midi_show_init_note_list(musicsheet, unit_time, playls)
            pyglet.clock.schedule_once(midi_file_play,
                                       current_piano_window.bars_drop_interval)
        current_piano_window.label.text = ''
        current_piano_window.label.draw()
        if window_mode == 0:
            current_piano_window.flip()

    def _midi_show_init_note_list(self, musicsheet, unit_time, playls, mode=0):
        for i in range(self.sheetlen):
            currentnote = musicsheet.notes[i]
            duration = unit_time * currentnote.duration
            interval = unit_time * musicsheet.interval[i]
            currentstart = self.start
            currentstop = self.start + duration
            if mode == 0:
                currentwav = 0
            else:
                currentwav = pygame.mixer.Sound(
                    f'{piano_config.sound_path}/{currentnote}.{piano_config.sound_format}'
                )
                note_volume = currentnote.volume / 127
                note_volume *= piano_config.global_volume
                currentwav.set_volume(note_volume)
            playls.append(
                [currentwav, currentstart, currentstop, 0, i, currentnote])
            if piano_config.note_mode == 'bars drop':
                self.bars_drop_time.append(
                    (currentstart - current_piano_window.bars_drop_interval,
                     currentnote))
            self.start += interval

    def mode_self_pc(self, dt):
        self._pc_read_pc_keyboard_special_key()
        self._pc_read_pc_keyboard_key()
        self._pc_read_stillplay_notes()
        if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
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
                    if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                        current_bar = self._pc_draw_note_bar(each)
                    else:
                        current_bar = None
                    if piano_config.draw_piano_keys:
                        self._pc_set_piano_key_color(each, current_bar)
            else:
                if each not in self.last:
                    self.changed = True
                    self.wavdic[each].play()
                    if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                        current_bar = self._pc_draw_note_bar(each)
                    else:
                        current_bar = None
                    if piano_config.draw_piano_keys:
                        self._pc_set_piano_key_color(each, current_bar)

    def _pc_draw_note_bar(self, each):
        current_note = mp.toNote(self.notedic[each])
        places = current_piano_window.note_place[current_note.degree - 21]
        current_bar = pyglet.shapes.BorderedRectangle(
            x=places[0] + current_piano_window.bar_offset_x,
            y=piano_config.bar_y,
            width=piano_config.bar_width,
            height=piano_config.bar_height,
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
        current_note = mp.toNote(self.notedic[each])
        current_piano_key = current_piano_window.piano_keys[current_note.degree
                                                            - 21]
        if piano_config.color_mode == 'normal':
            current_piano_key.color = piano_config.bar_color
        else:
            if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
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
            each.y += piano_config.bar_steps
            if each.y >= current_piano_window.screen_height:
                each.batch = None
                del self.plays[i]
                continue
            i += 1
        for k in self.still_hold_pc:
            current_hold_note, current_bar = k
            if current_hold_note in self.truecurrent:
                current_bar.height += piano_config.bar_hold_increase
            else:
                self.plays.append(current_bar)
                self.still_hold_pc.remove(k)

    def _pc_update_notes(self):
        self.changed = False
        if piano_config.delay:
            if piano_config.delay_only_read_current:
                notels = [self.notedic[t] for t in self.truecurrent]
            else:
                notels = [self.notedic[t] for t in self.stillplay_obj]
        else:
            notels = [self.notedic[t] for t in self.last]
        if piano_config.draw_piano_keys:
            if self.lastshow:
                for t in self.lastshow:
                    current_piano_window.piano_keys[
                        t.degree -
                        21].color = current_piano_window.initial_colors[
                            t.degree - 21]
        if notels:
            self.currentchord = mp.chord(notels)
            for k in self.currentchord:
                if piano_config.draw_piano_keys:
                    current_piano_key = current_piano_window.piano_keys[
                        k.degree - 21]
                    current_piano_key.color = piano_config.bar_color if piano_config.color_mode == 'normal' else current_piano_key.current_color
            self.currentchord.notes.sort(key=lambda x: x.degree)
            if self.currentchord != self.lastshow:
                self.lastshow = self.currentchord
                current_piano_window.label.text = str(self.currentchord.notes)
                if piano_config.show_chord and any(
                        type(t) == mp.note for t in self.currentchord):
                    chordtype = self._detect_chord(self.currentchord)

                    current_piano_window.label2.text = str(
                        chordtype
                    ) if not piano_config.sort_invisible else get_off_sort(
                        str(chordtype))
        else:
            self.lastshow = notels
            current_piano_window.label.text = str(notels)
            current_piano_window.label2.text = ''
        if piano_config.show_key:
            current_piano_window.label.text = str(self.truecurrent)

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
                                self.wavdic[str(each)].fadeout(
                                    piano_config.fadeout_ms)
                            self.stillplay.remove(each)
                    else:
                        if piano_config.draw_piano_keys:
                            current_piano_window.piano_keys[
                                each.degree -
                                21].color = piano_config.sustain_bar_color
                        if self.stillplay:
                            self.currentchord = mp.chord([
                                k for k in self.stillplay if k.sustain_pedal_on
                            ] + self.current_play)
                            self.currentchord.notes.sort(
                                key=lambda x: x.degree)
                            current_piano_window.label.text = str(
                                self.currentchord.notes)
                            if piano_config.show_chord and any(
                                    type(t) == mp.note
                                    for t in self.currentchord):
                                chordtype = self._detect_chord(
                                    self.currentchord)
                                current_piano_window.label2.text = str(
                                    chordtype
                                ) if not piano_config.sort_invisible else get_off_sort(
                                    str(chordtype))
                        else:
                            current_piano_window.label.text = '[]'
                            current_piano_window.label2.text = ''
                else:
                    if piano_config.draw_piano_keys:
                        current_piano_window.piano_keys[
                            each.degree -
                            21].color = piano_config.sustain_bar_color
                    if self.stillplay:
                        self.currentchord = mp.chord(self.stillplay)
                        self.currentchord.notes.sort(key=lambda x: x.degree)
                        current_piano_window.label.text = str(
                            self.currentchord.notes)
                        if piano_config.show_chord and any(
                                type(t) == mp.note for t in self.currentchord):
                            chordtype = self._detect_chord(self.currentchord)
                            current_piano_window.label2.text = str(
                                chordtype
                            ) if not piano_config.sort_invisible else get_off_sort(
                                str(chordtype))
                    else:
                        current_piano_window.label.text = '[]'
                        current_piano_window.label2.text = ''
            else:
                each.count_time = self.current_time

    def _midi_keyboard_update_notes(self):
        if (not self.sostenuto_pedal_on) and self.last != self.current_play:
            self.last = self.current_play.copy()
            if self.current_play:
                self.currentchord = mp.chord(
                    self.current_play
                ) if piano_config.delay_only_read_current else mp.chord(
                    self.stillplay)
                self.currentchord.notes.sort(key=lambda x: x.degree)
                current_piano_window.label.text = str(self.currentchord.notes)
                if piano_config.show_chord and any(
                        type(t) == mp.note for t in self.currentchord):
                    chordtype = self._detect_chord(self.currentchord)

                    current_piano_window.label2.text = str(
                        chordtype
                    ) if not piano_config.sort_invisible else get_off_sort(
                        str(chordtype))
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
                if piano_config.draw_piano_keys and piano_config.delay_only_read_current:
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
                if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                    places = current_piano_window.note_place[
                        current_note.degree - 21]
                    current_bar = pyglet.shapes.BorderedRectangle(
                        x=places[0] + current_piano_window.bar_offset_x,
                        y=piano_config.bar_y,
                        width=piano_config.bar_width,
                        height=piano_config.bar_height,
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
                if piano_config.draw_piano_keys:
                    current_piano_key = current_piano_window.piano_keys[
                        current_note.degree - 21]
                    if piano_config.color_mode == 'normal':
                        current_piano_key.color = piano_config.bar_color
                    else:
                        if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
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
                        current_sound = self.wavdic[str(current_note)]
                        current_sound.set_volume(self.soft_pedal_volume_ratio *
                                                 velocity / 127)
                        current_sound.play()
            elif status == 176:
                if note_number == 64:
                    if velocity >= 64:
                        if piano_config.delay_only_read_current:
                            self.stillplay = copy(self.current_play)
                            piano_config.delay_only_read_current = False
                    else:
                        if not piano_config.delay_only_read_current:
                            if piano_config.draw_piano_keys:
                                for each in self.stillplay:
                                    pyglet.clock.schedule_once(
                                        piano_key_reset,
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
                            if piano_config.draw_piano_keys:
                                for each in self.stillplay:
                                    pyglet.clock.schedule_once(
                                        piano_key_reset,
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
        if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
            i = 0
            while i < len(self.plays):
                each = self.plays[i]
                each.y += piano_config.bar_steps
                if each.y >= current_piano_window.screen_height:
                    each.batch = None
                    del self.plays[i]
                    continue
                i += 1
            for k in self.still_hold:
                current_hold_note, current_bar = k
                if current_hold_note in self.current_play:
                    current_bar.height += piano_config.bar_hold_increase
                else:
                    self.plays.append(current_bar)
                    self.still_hold.remove(k)

    def _midi_keyboard_read_pc_keyboard_key(self):
        if current_piano_window.keyboard_handler[key.LSHIFT]:
            current_piano_window.label_midi_device.text = self.current_midi_device
        if current_piano_window.keyboard_handler[key.LCTRL]:
            current_piano_window.label_midi_device.text = ''
        if piano_config.config_enable:
            if piano_config.play_use_soundfont:
                self.detect_sf2_config(1)

    def mode_midi_show(self, dt):
        if not self.paused:
            self._midi_show_playing()
        else:
            self._midi_show_pause()
        if self.finished:
            self._midi_show_finished()

    def _midi_show_playing(self):
        self.currentime = time.time() - self.startplay
        if piano_config.note_mode == 'bars drop':
            self._midi_show_draw_notes_bars_drop_mode()
        for k in range(self.sheetlen):
            nownote = self.playls[k]
            self._midi_show_play_current_note(nownote, k)

        self.playnotes = [
            self.wholenotes[x[4]] for x in self.playls if x[3] == 1
        ]
        if self.playnotes:
            self._midi_show_update_notes()
        self._midi_show_playing_read_pc_keyboard_key()

        if piano_config.note_mode == 'bars':
            self._midi_show_draw_notes_hit_key_bars_mode()
        elif piano_config.note_mode == 'bars drop':
            self._midi_show_draw_notes_hit_key_bars_drop_mode()

    def _midi_show_play_current_note(self, nownote, k):
        current_sound, start_time, stop_time, situation, number, current_note = nownote
        if situation != 2:
            if situation == 0:
                if self.currentime >= start_time:
                    if not self.play_midi_file:
                        current_sound.play()
                    nownote[3] = 1
                    if piano_config.show_music_analysis:
                        if self.show_music_analysis_list:
                            current_music_analysis = self.show_music_analysis_list[
                                0]
                            if k == current_music_analysis[0]:
                                current_piano_window.music_analysis_label.text = current_music_analysis[
                                    1]
                                del self.show_music_analysis_list[0]
                    if piano_config.note_mode == 'bars':
                        self._midi_show_draw_notes_bars_mode(current_note)
                    elif piano_config.note_mode != 'bars drop':
                        self._midi_show_set_piano_key_color(current_note)
            elif situation == 1:
                if self.currentime >= stop_time:
                    if not self.play_midi_file:
                        current_sound.fadeout(
                            current_piano_window.show_delay_time)
                    nownote[3] = 2
                    if k == self.sheetlen - 1:
                        self.finished = True

    def _midi_show_draw_notes_bars_drop_mode(self):
        if self.bars_drop_time:
            j = 0
            while j < len(self.bars_drop_time):
                next_bar_drop = self.bars_drop_time[j]
                if self.currentime >= next_bar_drop[0]:
                    current_note = next_bar_drop[1]
                    places = current_piano_window.note_place[
                        current_note.degree - 21]
                    current_bar = pyglet.shapes.BorderedRectangle(
                        x=places[0] + current_piano_window.bar_offset_x,
                        y=current_piano_window.screen_height,
                        width=piano_config.bar_width,
                        height=piano_config.bar_unit * current_note.duration /
                        (self.bpm / 130),
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
                    self.plays.append(current_bar)
                    del self.bars_drop_time[j]
                    continue
                j += 1

    def _midi_show_draw_notes_bars_mode(self, current_note):
        places = current_piano_window.note_place[current_note.degree - 21]
        current_bar = pyglet.shapes.BorderedRectangle(
            x=places[0] + current_piano_window.bar_offset_x,
            y=piano_config.bar_y,
            width=piano_config.bar_width,
            height=piano_config.bar_unit * current_note.duration /
            (self.bpm / 130),
            color=current_note.own_color if piano_config.use_track_colors else
            (piano_config.bar_color if piano_config.color_mode == 'normal' else
             (random.randint(0, 255), random.randint(0, 255),
              random.randint(0, 255))),
            batch=current_piano_window.batch,
            group=current_piano_window.play_highlight,
            border=piano_config.bar_border,
            border_color=piano_config.bar_border_color)
        current_bar.opacity = 255 * (
            current_note.volume / 127
        ) if piano_config.opacity_change_by_velocity else piano_config.bar_opacity
        self.plays.append(current_bar)
        current_piano_window.piano_keys[current_note.degree -
                                        21].color = current_bar.color

    def _midi_show_update_notes(self):
        self.playnotes.sort(key=lambda x: x.degree)
        if self.playnotes != self.lastshow:
            if piano_config.draw_piano_keys and piano_config.note_mode != 'bars drop':
                if self.lastshow:
                    for each in self.lastshow:
                        if each not in self.playnotes:
                            current_piano_window.piano_keys[
                                each.degree -
                                21].color = current_piano_window.initial_colors[
                                    each.degree - 21]
            self.lastshow = self.playnotes
            if piano_config.show_notes:
                current_piano_window.label.text = str(self.playnotes)
            if piano_config.show_chord and any(
                    type(t) == mp.note for t in self.playnotes):
                chordtype = self._detect_chord(self.playnotes)
                current_piano_window.label2.text = str(
                    chordtype
                ) if not piano_config.sort_invisible else get_off_sort(
                    str(chordtype))

    def _midi_show_set_piano_key_color(self, current_note):
        current_piano_key = current_piano_window.piano_keys[current_note.degree
                                                            - 21]
        if piano_config.use_track_colors:
            current_piano_key.color = current_note.own_color
        else:
            if piano_config.color_mode == 'normal':
                current_piano_key.color = piano_config.bar_color
            else:
                current_piano_key.color = (random.randint(0, 255),
                                           random.randint(0, 255),
                                           random.randint(0, 255))

    def _midi_show_playing_read_pc_keyboard_key(self):
        if current_piano_window.keyboard_handler[
                current_piano_window.pause_key]:
            if self.play_midi_file:
                if piano_config.use_soundfont:
                    if piano_config.render_as_audio:
                        if pygame.mixer.get_busy():
                            pygame.mixer.pause()
                            self.paused = True
                    else:
                        if current_piano_window.current_sf2_player.playing:
                            current_piano_window.current_sf2_player.pause()
                            self.paused = True
                else:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                        self.paused = True
            else:
                self.paused = True
            if self.paused:
                self.pause_start = time.time()
                current_piano_window.message_label = True
                current_piano_window.label3.text = language_patch.ideal_piano_language_dict[
                    'pause'].format(unpause_key=piano_config.unpause_key)

    def _midi_show_draw_notes_hit_key_bars_mode(self):
        i = 0
        while i < len(self.plays):
            each = self.plays[i]
            each.y += current_piano_window.bar_steps
            if each.y >= current_piano_window.screen_height:
                each.batch = None
                del self.plays[i]
                continue
            i += 1

    def _midi_show_draw_notes_hit_key_bars_drop_mode(self):
        i = 0
        while i < len(self.plays):
            each = self.plays[i]
            each.y -= current_piano_window.bar_steps
            if not each.hit_key and each.y <= piano_config.bars_drop_place:
                each.hit_key = True
                if piano_config.draw_piano_keys:
                    current_piano_window.piano_keys[
                        each.num].color = each.color
            if each.height + each.y <= current_piano_window.piano_height:
                each.batch = None
                if piano_config.draw_piano_keys:
                    current_piano_window.piano_keys[
                        each.num].color = current_piano_window.initial_colors[
                            each.num]
                del self.plays[i]
                continue
            i += 1

    def _midi_show_pause(self):
        if current_piano_window.keyboard_handler[
                current_piano_window.unpause_key]:
            if self.play_midi_file:
                if piano_config.use_soundfont:
                    if piano_config.render_as_audio:
                        pygame.mixer.unpause()
                    else:
                        current_piano_window.current_sf2_player.unpause()
                else:
                    pygame.mixer.music.unpause()
            self.paused = False
            current_piano_window.message_label = False
            pause_stop = time.time()
            pause_time = pause_stop - self.pause_start
            self.startplay += pause_time

    def _midi_show_finished(self):
        if piano_config.draw_piano_keys and piano_config.note_mode != 'bars drop':
            if self.lastshow:
                for t in self.lastshow:
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
            if piano_config.note_mode == 'bars' or piano_config.note_mode == 'bars drop':
                self.plays.clear()
                if piano_config.note_mode == 'bars drop':
                    self.bars_drop_time.clear()
            if piano_config.draw_piano_keys:
                for k in range(len(current_piano_window.piano_keys)):
                    current_piano_window.piano_keys[
                        k].color = current_piano_window.initial_colors[k]
            self.playls.clear()
            current_piano_window.label.text = ''
            current_piano_window.redraw()
            self.playls = self._midi_show_init(self.musicsheet,
                                               self.unit_time,
                                               self.musicsheet.start_time,
                                               window_mode=1)
            self.startplay = time.time()
            self.lastshow = None
            self.playnotes.clear()
            self.finished = False


current_piano_engine = piano_engine()
current_piano_window = piano_window()
pyglet.clock.schedule_interval(update, 1 / piano_config.fps)
pyglet.app.run()
