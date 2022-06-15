# basic screen settings

screen_size = (1300, 650)
background_image = 'resources/white.png'
background_size = None
width_or_height_first = True
piano_image = 'resources/piano.png'
piano_size = None
message_color = (0, 0, 0, 255)
fonts_size = 23
label1_place = (300, 400)
label2_place = (300, 350)
label3_place = (300, 450)
label_anchor_x = 'left'
label_anchor_y = 'center'
label_width = 1000
fonts = 'Consolas'
bold = True
go_back_image = 'resources/go_back.png'
go_back_place = 50, 550
self_play_image = 'resources/play.png'
self_play_place = 50, 480
self_midi_image = 'resources/midi_keyboard.png'
self_midi_place = 50, 410
play_midi_image = 'resources/play_midi.png'
play_midi_place = 50, 340
settings_image = 'resources/settings.png'
settings_place = 50, 270
button_resize_num = 2.3
fps = 60

# the key settings for playing 88 notes (from A0 to C8)
# (if you have sound files that beyond these range then you can
# modify this dictionary to play them)

key_settings = {
    'z': 'A#1',
    'x': 'B1',
    'c': 'C2',
    'v': 'C#2',
    'b': 'D2',
    'n': 'D#2',
    'm': 'E2',
    ',': 'F2',
    '.': 'F#2',
    '/': 'G2',
    'a': 'G#2',
    's': 'A2',
    'd': 'A#2',
    'f': 'B2',
    'g': 'C3',
    'h': 'C#3',
    'j': 'D3',
    'k': 'D#3',
    'l': 'E3',
    ';': 'F3',
    "'": 'F#3',
    'enter': 'G3',
    'tab': 'G#3',
    'q': 'A3',
    'w': 'A#3',
    'e': 'B3',
    'r': 'C4',
    't': 'C#4',
    'y': 'D4',
    'u': 'D#4',
    'i': 'E4',
    'o': 'F4',
    'p': 'F#4',
    '[': 'G4',
    ']': 'G#4',
    '\\': 'A4',
    '`': 'A#4',
    '1': 'B4',
    '2': 'C5',
    '3': 'C#5',
    '4': 'D5',
    '5': 'D#5',
    '6': 'E5',
    '7': 'F5',
    '8': 'F#5',
    '9': 'G5',
    '0': 'G#5',
    '-': 'A5',
    '=': 'A#5',
    'backspace': 'B5',
    'f1': 'C6',
    'f2': 'C#6',
    'f3': 'D6',
    'f4': 'D#6',
    'f5': 'E6',
    'f6': 'F6',
    'f7': 'F#6',
    'f8': 'G6',
    'f9': 'G#6',
    'f10': 'A6',
    'f11': 'A#6',
    'f12': 'B6'
}

midi_device_id = 1

# operation key settings for pause, unpause, repeat and so on
pause_key = 'space'
repeat_key = 'ctrl'
unpause_key = 'enter'
pause_key_clear_notes = False

# these are the init parameters of the mixer
frequency = 44100
size = -16
channel = 2
buffer = 1024
max_num_channels = 100
global_volume = 0.6

# if delay is set to True, when you are self playing, the sounds will
# last for delay_time seconds
delay = True
delay_time = 3
fadeout_ms = 100

# touch interval is when the sound is still on delay, if you re-press
# the key for the same key for that sound, the time interval between
# the last time you press the key and this time is beyond this interval,
# then the sound will stop and replay again, this paramter is used
# for pressing keys' sensitivity.
touch_interval = 0.1

# if this parameter is set to True,
# then it only reads the key you are actually pressing now,
# not to include the sounds on delay but you are not pressing
delay_only_read_current = True

# the suffix of the sound files
sound_format = 'mp3'

# the path of the sounds folder
sound_path = 'resources/sounds'

# when the mode is in 'show' mode, the delay time for the sounds
show_delay_time = 1

# these are the parameters for chord types detections
# change_from_first: detection result is preferentially chosen as changed from another chord(flat or sharp some notes)
# original_first: detection result is preferentially chosen as a variation of the original position of the chord(i.e. no inversion or any changes to the notes of the chord)
inv_num = False
change_from_first = True
original_first = True
same_note_special = False
whole_detect = True
return_fromchord = False
poly_chord_first = False
root_position_return_first = True
alter_notes_show_degree = True

# if this is set to True, then you enable the config key during the playing
config_enable = True

# if you press the config key with the following keys, those keys will be able to adjust settings in realtime.
config_key = 'lctrl'

# volume change keys
volume_up = '='
volume_down = '-'

# volume change of each volume up/down
volume_change_unit = 0.01

# if delay is set to True before you press, then it will change to False, if False before then set to True
change_delay = 'd'
change_read_current = 'c'
change_pause_key_clear_notes = 'x'

# load sounds from the folders of sound paths when playing or not
load_sound = True

# show_key set to True will show what keyboard keys you are pressing
show_key = False

# detect chord types when the current notes change
show_chord = True
show_notes = True

# the parameters of the function split_melody
melody_tol = 10
chord_tol = 9
get_off_overlap_notes = False
average_degree_length = 8
melody_degree_tol = 'B4'

# notes showing mode: choose one from 'bars' and 'bars drop',
# or you can set as other names, and turn on the draw piano keys mode
note_mode = 'bars drop'
bar_width = 14
bar_height = 20
bar_color = (124, 252, 0)
sustain_bar_color = (124, 200, 0)
bar_y = 178
bar_offset_x = 6
bar_opacity = 160
opacity_change_by_velocity = True
# color mode: choose one from 'normal' and 'rainbow'
color_mode = 'normal'
bar_steps = 6
bar_unit = 400
bar_hold_increase = 5
bars_drop_interval = 2
bars_drop_place = 173
adjust_ratio = 62
bar_border = 5
bar_border_color = (100, 100, 100)

# when play midi files, if you choose to merge all tracks, get_off_drums
# set to True will not merge the drum tracks if your midi file has
get_off_drums = True

sort_invisible = False

play_as_midi = True

draw_piano_keys = True

white_key_width = 23
white_key_height = 138
white_key_interval = 25
white_key_y = 37
white_keys_number = 52
white_key_start_x = 0
white_key_color = (255, 255, 255)

black_key_width = 15
black_key_height = 90
black_key_y = 85
black_key_first_x = 18
black_key_start_x = 64.467
black_key_color = (0, 0, 0)

black_keys_set = [0, 30, 43.85, 28.67, 28.48]
black_keys_set_interval = 43.75
black_keys_set_num = 7

piano_key_border = 0
piano_key_border_color = (100, 100, 100)

piano_background_image = 'resources/piano_background.png'

show_music_analysis = False
music_analysis_file = None
music_analysis_place = (250, 500)
key_header = 'current key: '
music_analysis_width = 1300
music_analysis_fonts_size = 20

use_track_colors = True
tracks_colors = [(0, 255, 0), (255, 255, 0), (0, 0, 255), (0, 255, 255),
                 (255, 0, 255), (0, 128, 0), (0, 191, 255), (0, 255, 127),
                 (0, 128, 128), (0, 0, 128), (255, 215, 0), (255, 165, 0),
                 (124, 252, 0), (238, 130, 238), (218, 112, 214),
                 (255, 20, 147)]
use_default_tracks_colors = True
pitch_range = ('A0', 'C8')

use_soundfont = False
play_use_soundfont = False
sf2_path = 'resources/gm.sf2'
bank = 0
preset = 0
sf2_duration = 6
sf2_decay = 1
sf2_volume = 100
sf2_mode = 0

soft_pedal_volume = 0.2

render_as_audio = False

language = 'English'

show_chord_accidentals = 'sharp'

show_chord_details = False
chord_details_label_place = (750, 500)
chord_details_label_anchor_x = 'left'
chord_details_label_anchor_y = 'baseline'
chord_details_font_size = 15
chord_details_label_width = 500

show_current_detect_key = False
current_detect_key_label_place = (230, 550)
current_detect_key_label_anchor_x = 'left'
current_detect_key_label_anchor_y = 'baseline'
current_detect_key_font_size = 15
current_detect_key_label_width = 1000
major_minor_preference = False
most_appear_num = 5
current_detect_key_limit = 100
