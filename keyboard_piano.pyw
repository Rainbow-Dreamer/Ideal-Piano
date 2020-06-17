import pygame, keyboard, os, time, sys, pyglet
abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.append(abs_path)
with open('config.py', encoding='utf-8') as f:
    exec(f.read())
from musicpy.musicpy import *
import pygame.midi
import browse
from pyglet.window import mouse
os.chdir(abs_path)

class Button:
    def __init__(self, img, x, y):
        self.img = pyglet.resource.image(img)
        self.img.width /= 3
        self.img.height /= 3
        self.x = x
        self.y = y

    def MakeButton(self):
        return pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)

    def get_range(self):
        height, width = self.img.height, self.img.width
        return [self.x, self.x + width], [self.y, self.y + height]

    def inside(self):
        range_x, range_y = self.get_range()
        return range_x[0] <= mouse_pos[0] <= range_x[1] and range_y[
            0] <= mouse_pos[1] <= range_y[1]


screen_width, screen_height = screen_size
show_delay_time = int(show_delay_time * 1000)
pressed = keyboard.is_pressed
pygame.mixer.init(frequency, size, channel, buffer)
pyglet.resource.path = [abs_path]
pyglet.resource.reindex()
background = pyglet.resource.image(background_image)
if not background_size:
    ratio_background = screen_width / background.width
    background.width = screen_width
    background.height *= ratio_background
else:
    background.width, background.height = background_size

image = pyglet.resource.image(piano_image)
if not piano_size:
    ratio = screen_width / image.width
    image.width = screen_width
    image.height *= ratio
else:
    image.width, image.height = piano_size
playing = pyglet.resource.image(notes_image)
playing.width /= notes_resize_num
playing.height /= notes_resize_num
plays = [pyglet.sprite.Sprite(playing, x=j[0], y=j[1]) for j in note_place]
go_back = Button(go_back_image, *go_back_place)
button_go_back = go_back.MakeButton()
self_play = Button(self_play_image, *self_play_place)
button_play = self_play.MakeButton()
self_midi = Button(self_midi_image, *self_midi_place)
button_self_midi = self_midi.MakeButton()
play_midi = Button(play_midi_image, *play_midi_place)
button_play_midi = play_midi.MakeButton()
window = pyglet.window.Window(*screen_size)

label = pyglet.text.Label('',
                          font_name=fonts,
                          font_size=fonts_size,
                          x=label1_place[0],
                          y=label1_place[1],
                          color=message_color,
                          anchor_x='center',
                          anchor_y='center')
label2 = pyglet.text.Label('',
                           font_name=fonts,
                           font_size=fonts_size,
                           x=label2_place[0],
                           y=label2_place[1],
                           color=message_color,
                           anchor_x='center',
                           anchor_y='center')
label3 = pyglet.text.Label('',
                           font_name=fonts,
                           font_size=fonts_size,
                           x=label3_place[0],
                           y=label3_place[1],
                           color=message_color,
                           anchor_x='center',
                           anchor_y='center')


def load(dic, path, file_format, volume):
    wavedict = {
        i: pygame.mixer.Sound(f'{path}{dic[i]}.{file_format}')
        for i in dic
    }
    if volume != None:
        [wavedict[x].set_volume(volume) for x in wavedict]
    return wavedict


def configkey(q):
    return pressed(f'{config_key} + {q}')


def configshow(content):
    label.text = str(content)


def switchs(q, name):
    if configkey(q):
        globals()[name] = not globals()[name]
        configshow(f'{name} changes to {globals()[name]}')


mouse_pos = 0, 0
is_click = True
first_time = True
message_label = False
notedic = key_settings
is_click = False
mode_num = None
func = None
click_mode = None
midi_device_load = False
batch = pyglet.graphics.Batch()


def has_load():
    global midi_device_load
    midi_device_load = True


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos
    mouse_pos = x, y


@window.event
def on_mouse_press(x, y, button, modifiers):
    global is_click
    global click_mode
    if go_back.inside() & button & mouse.LEFT and not first_time:
        if mode_num in [0, 1, 2]:
            global lastshow
            global plays
            for each in plays:
                each.batch = None
        is_click = True
        click_mode = None
    if self_play.inside() & button & mouse.LEFT and first_time:
        click_mode = 0
    if self_midi.inside() & button & mouse.LEFT and first_time:
        click_mode = 1
    if play_midi.inside() & button & mouse.LEFT and first_time:
        click_mode = 2


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    image.blit(0, 0)
    button_go_back.draw()
    if first_time:
        global is_click
        global mode_num
        global func
        button_play.draw()
        button_self_midi.draw()
        button_play_midi.draw()
        if mode_num is None:
            if click_mode == 0:
                mode_num = 0
                label.text = 'loading sound samples, please wait...'
                label.draw()
            elif click_mode == 1:
                mode_num = 1
                label.text = 'loading sound samples, please wait...'
                label.draw()
            elif click_mode == 2:
                mode_num = 2

        else:
            if mode_num == 0:
                init_self_pc()
                label.text = 'sounds loading finished'
                label.draw()
                func = mode_self_pc
                not_first()
                pyglet.clock.schedule_interval(func, 1 / 120)
            elif mode_num == 1:
                try:
                    init_self_midi()
                    label.text = 'sounds loading finished'
                    label.draw()
                    func = mode_self_midi
                    not_first()
                    pyglet.clock.schedule_interval(func, 1 / 120)
                except:
                    label.text = 'there is no midi input devices, please check'
                    mode_num = 3
                    reset_click_mode()
                    label.draw()

            elif mode_num == 2:
                init_result = init_show()
                if init_result == 'back':
                    mode_num = 4
                else:
                    func = mode_show
                    not_first()
                    pyglet.clock.schedule_interval(func, 1 / 120)

            elif mode_num == 3:
                time.sleep(2)
                label.text = ''
                mode_num = None
            elif mode_num == 4:
                label.text = ''
                mode_num = None
                reset_click_mode()

    else:

        if is_click:
            is_click = False
            not_first()
            label.text = ''
            label2.text = ''

            pyglet.clock.unschedule(func)
            mode_num = None
        else:
            if mode_num == 0:
                if label2.text != '':
                    batch.draw()
            elif mode_num == 1:
                batch.draw()
            elif mode_num == 2:
                batch.draw()
        label.draw()
        label2.draw()
        if message_label:
            label3.draw()


currentchord = chord([])
playnotes = []


def reset_click_mode():
    global click_mode
    click_mode = None


def not_first():
    global first_time
    first_time = not first_time


def mode_self_pc(dt):
    global stillplay
    global last
    global changed
    global lastshow
    global currentchord
    global global_volume
    if config_enable:
        if configkey(volume_up):
            global_volume += volume_change_unit
            [wavdic[j].set_volume(global_volume) for j in wavdic]
            configshow(f'volume up to {int(global_volume*100)}%')
        if configkey(volume_down):
            global_volume -= volume_change_unit
            [wavdic[j].set_volume(global_volume) for j in wavdic]
            configshow(f'volume down to {int(global_volume*100)}%')
        switchs(change_delay, 'delay')
        switchs(change_read_current, 'delay_only_read_current')
        switchs(change_pause_key_clear_notes, 'pause_key_clear_notes')
    if keyboard.is_pressed(pause_key):
        [wavdic[x].stop() for x in last]
        if pause_key_clear_notes:
            if delay:
                stillplay = []
    current = keyboard.get_hotkey_name().split('+')
    current = [i for i in current if i in wavdic]
    if delay:
        stillplay_obj = [x[0] for x in stillplay]
        if delay_only_read_current or show_key:
            truecurrent = current.copy()
    for each in current:
        if delay:
            if each in stillplay_obj:
                inds = stillplay_obj.index(each)
                if not stillplay[inds][2] and time.time(
                ) - stillplay[inds][1] > touch_interval:
                    wavdic[each].stop()
                    stillplay.pop(inds)
                    stillplay_obj.pop(inds)
            else:
                changed = True
                wavdic[each].play()
                stillplay.append([each, time.time(), True])
                stillplay_obj.append(each)
        else:
            if each not in last:
                changed = True
                wavdic[each].play()
    for j in last:
        if j not in current:

            if delay:
                if j in stillplay_obj:
                    ind = stillplay_obj.index(j)
                    stillobj = stillplay[ind]
                    if time.time() - stillobj[1] > delay_time:
                        changed = True
                        wavdic[j].stop()
                        stillplay.pop(ind)
                        stillplay_obj.pop(ind)
                    else:
                        stillplay[ind][2] = False
                        current.append(j)
                else:
                    changed = True
                    wavdic[j].stop()
            else:
                changed = True
                wavdic[j].stop()
    last = current
    if changed:
        changed = False
        if delay:
            if delay_only_read_current:
                notels = [notedic[t] for t in truecurrent]
            else:
                notels = [notedic[t] for t in stillplay_obj]
        else:
            notels = [notedic[t] for t in last]
        if lastshow:
            for t in lastshow:
                plays[t.degree - 21].batch = None
        if notels:
            currentchord = chord(notels)
            for k in currentchord:
                plays[k.degree - 21].batch = batch
        if show_chord:
            if notels:
                currentchord.notes.sort(key=lambda x: x.degree)
                if currentchord != lastshow:
                    lastshow = currentchord
                    label.text = str(currentchord.notes)
                    chordtype = detect(currentchord,
                                       ignore_sort_from=ignore_sort_from,
                                       change_from_first=change_from_first,
                                       original_first=original_first,
                                       ignore_add_from=ignore_add_from,
                                       same_note_special=same_note_special,
                                       two_show_interval=two_show_interval)

                    label2.text = str(chordtype)
            else:
                lastshow = notels
                label.text = str(notels)
                label2.text = ''
        else:
            lastshow = notels
            label.text = str(notels)
        if show_key:
            label.text = str(truecurrent)


def mode_self_midi(dt):
    global last
    global current_play
    if last != current_play:
        for k in last:
            plays[k.degree - 21].batch = None
        last = current_play.copy()
        if current_play:
            for each in current_play:
                plays[each.degree - 21].batch = batch
            currentchord = chord(current_play)
            currentchord.notes.sort(key=lambda x: x.degree)
            label.text = str(currentchord.notes)
            chordtype = detect(currentchord,
                               ignore_sort_from=ignore_sort_from,
                               change_from_first=change_from_first,
                               original_first=original_first,
                               ignore_add_from=ignore_add_from,
                               same_note_special=same_note_special,
                               two_show_interval=two_show_interval)

            label2.text = str(chordtype)
        else:
            label.text = '[]'
            label2.text = ''

    if device.poll():
        event = device.read(1)[0]
        data = event[0]
        timestamp = event[1]
        note_number = data[1]
        velocity = data[2]
        current_note = degree_to_note(note_number)
        if velocity == 0:
            plays[note_number - 21].batch = None
            if current_note in current_play:
                current_play.remove(current_note)
                #wavdic[str(current_note)].stop()
        else:
            if current_note not in current_play:
                current_play.append(current_note)
                current_sound = wavdic[str(current_note)]
                current_sound.set_volume(velocity / 127)
                current_sound.play(maxtime=midi_delay_time)


paused = False
pause_start = 0


def mode_show(dt):
    global startplay
    global lastshow
    global finished
    global playls
    global paused
    global pause_start
    global message_label
    global playnotes
    global get_off_melody
    if not paused:
        currentime = time.time() - startplay
        for k in range(sheetlen):

            nownote = playls[k]
            situation = nownote[3]
            if situation != 2:
                if situation == 0:
                    if currentime >= nownote[1]:
                        nownote[0].play()
                        playls[k][3] = 1
                elif situation == 1:
                    if currentime >= nownote[2]:
                        nownote[0].fadeout(show_delay_time)
                        playls[k][3] = 2
                        if k == sheetlen - 1:
                            finished = True
        time.sleep(delay_each_loop)
        if show_chord:
            playnotes = [wholenotes[x[4]] for x in playls if x[3] == 1]
            if playnotes:
                playnotes.sort(key=lambda x: x.degree)
                if playnotes != lastshow:
                    if lastshow:
                        for each in lastshow:
                            plays[each.degree - 21].batch = None
                    for i in playnotes:
                        plays[i.degree - 21].batch = batch
                    lastshow = playnotes
                    label.text = str(playnotes)
                    if get_off_melody:
                        playnotes = [
                            x for x in playnotes
                            if x.number not in melody_notes
                        ]
                        if playnotes:
                            chordtype = detect(
                                playnotes,
                                ignore_sort_from=ignore_sort_from,
                                change_from_first=change_from_first,
                                original_first=original_first,
                                ignore_add_from=ignore_add_from,
                                same_note_special=same_note_special,
                                two_show_interval=two_show_interval)
                            label2.text = str(chordtype)
                    else:
                        chordtype = detect(playnotes,
                                           ignore_sort_from=ignore_sort_from,
                                           change_from_first=change_from_first,
                                           original_first=original_first,
                                           ignore_add_from=ignore_add_from,
                                           same_note_special=same_note_special,
                                           two_show_interval=two_show_interval)
                        label2.text = str(chordtype)

        if keyboard.is_pressed(pause_key):
            paused = True
            pause_start = time.time()
            message_label = True
            label3.text = f'paused, press {unpause_key} to unpause'
    else:
        if keyboard.is_pressed(unpause_key):
            paused = False
            message_label = False
            pause_stop = time.time()
            pause_time = pause_stop - pause_start
            startplay += pause_time
    if finished:
        if show_chord:
            label2.text = ''
        for each in plays:
            each.batch = None
        label.text = f'music playing finished, press {repeat_key} to listen again, or press {exit_key} to exit'
        if keyboard.is_pressed(repeat_key):
            playls = initialize(musicsheet, unit_time)
            startplay = time.time()
            lastshow = None
            finished = False
        if keyboard.is_pressed(exit_key):
            sys.exit(0)


def initialize(musicsheet, unit_time):
    playls = []
    start = 0
    for i in range(sheetlen):
        currentnote = musicsheet.notes[i]
        currentwav = pygame.mixer.Sound(
            f'{sound_path}{currentnote}.{sound_format}')
        duration = unit_time * currentnote.duration
        interval = unit_time * musicsheet.interval[i]
        currentstart = start
        currentstop = start + duration
        note_volume = currentnote.volume / 127
        note_volume *= global_volume
        currentwav.set_volume(note_volume)
        playls.append([currentwav, currentstart, currentstop, 0, i])
        start += interval
    return playls


def init_self_pc():
    global wavdic
    global last
    global changed
    if delay:
        global stillplay
    global lastshow
    pygame.mixer.set_num_channels(maxinum_channels)
    wavdic = load(notedic, sound_path, sound_format, global_volume)
    last = []
    changed = False
    if delay:
        stillplay = []
    lastshow = None


def init_self_midi():
    global current_play
    global midi_delay_time
    global wavdic
    global device
    global last
    if not midi_device_load:
        has_load()
        pygame.mixer.set_num_channels(maxinum_channels)
        pygame.midi.init()
        device = pygame.midi.Input(midi_device_id)
        midi_delay_time = int(delay_time * 1000)
    notenames = os.listdir(sound_path)
    notenames = [x[:x.index('.')] for x in notenames]
    wavdic = load({i: i
                   for i in notenames}, sound_path, sound_format,
                  global_volume)
    current_play = []
    last = current_play.copy()


def browse_reset():
    browse.file_path, browse.track_get, browse.track_ind_get, browse.read_result, browse.set_bpm, browse.off_melody = None, None, None, None, None, 0


melody_notes = []


def init_show():
    global playls
    global startplay
    global lastshow
    global finished
    global sheetlen
    global wholenotes
    global musicsheet
    global unit_time
    global get_off_melody
    global melody_notes
    browse.setup()
    path = browse.file_path
    if browse.action == 1:
        browse.action = 0
        browse_reset()
        return 'back'
    if path and browse.read_result:
        play_interval = browse.interval
        if browse.read_result != 'error':
            bpm2, musicsheet = browse.read_result
            if browse.set_bpm:
                bpm2 = float(browse.set_bpm)
            sheetlen = browse.sheetlen

        else:
            browse_reset()
            return 'back'

        if bpm is None:
            bpm_to_use = bpm2
        else:
            bpm_to_use = bpm
    else:
        browse_reset()
        return 'back'

    get_off_melody = browse.off_melody
    if get_off_melody:
        for k in range(sheetlen):
            musicsheet.notes[k].number = k
        melody_notes = split_melody(musicsheet)

    browse_reset()
    if play_interval is not None:
        browse.interval = None

        play_start, play_stop = int(sheetlen * (play_interval[0] / 100)), int(
            sheetlen * (play_interval[1] / 100))
        musicsheet = musicsheet[play_start:play_stop + 1]
        sheetlen = play_stop + 1 - play_start
    if show_change_pitch != None:
        musicsheet = musicsheet.up(show_change_pitch)
    if show_modulation != None:
        musicsheet = modulation(musicsheet, eval(show_modulation[0]),
                                eval(show_modulation[1]))

    if sheetlen == 0:
        return 'back'
    pygame.mixer.set_num_channels(sheetlen)
    wholenotes = musicsheet.notes
    unit_time = 60 / bpm_to_use

    # every object in playls has a situation flag at the index of 3,
    # 0 means has not been played yet, 1 means it has started playing,
    # 2 means it has stopped playing
    playls = initialize(musicsheet, unit_time)
    startplay = time.time()
    lastshow = None
    finished = False
    func = mode_show


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()