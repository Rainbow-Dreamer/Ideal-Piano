# basic screen settings

screen_size = (1300, 650)
background_image = 'white.png'
background_size = None
piano_image = 'piano.png'
piano_size = None
message_color = (0, 0, 0, 255)
fonts_size = 23
label1_place = (300, 400)
label2_place = (300, 350)
label3_place = (300, 450)
label_anchor_x = 'left'
label_anchor_y = 'center'
fonts = 'Cambria'
bold = True
notes_image = 'playing.png'
notes_resize_num = 1.2
go_back_image = 'go_back.png'
go_back_place = 50, 550
self_play_image = 'play.png'
self_play_place = 50, 480
self_midi_image = 'midi_keyboard.png'
self_midi_place = 50, 410
play_midi_image = 'play_midi.png'
play_midi_place = 50, 340
button_resize_num = 2.3
fps = 120

# the key settings for playing 88 notes (from A1 to C9)
# (if you have sound files that beyond these range then you can
# modify this dictionary to play them)

key_settings = {
    'z': 'A#2',
    'x': 'B2',
    'c': 'C3',
    'v': 'C#3',
    'b': 'D3',
    'n': 'D#3',
    'm': 'E3',
    ',': 'F3',
    '.': 'F#3',
    '/': 'G3',
    'a': 'G#3',
    's': 'A3',
    'd': 'A#3',
    'f': 'B3',
    'g': 'C4',
    'h': 'C#4',
    'j': 'D4',
    'k': 'D#4',
    'l': 'E4',
    ';': 'F4',
    "'": 'F#4',
    'enter': 'G4',
    'tab': 'G#4',
    'q': 'A4',
    'w': 'A#4',
    'e': 'B4',
    'r': 'C5',
    't': 'C#5',
    'y': 'D5',
    'u': 'D#5',
    'i': 'E5',
    'o': 'F5',
    'p': 'F#5',
    '[': 'G5',
    ']': 'G#5',
    '\\': 'A5',
    '`': 'A#5',
    '1': 'B5',
    '2': 'C6',
    '3': 'C#6',
    '4': 'D6',
    '5': 'D#6',
    '6': 'E6',
    '7': 'F6',
    '8': 'F#6',
    '9': 'G6',
    '0': 'G#6',
    '-': 'A6',
    '=': 'A#6',
    'backspace': 'B6',
    'f1': 'C7',
    'f2': 'C#7',
    'f3': 'D7',
    'f4': 'D#7',
    'f5': 'E7',
    'f6': 'F7',
    'f7': 'F#7',
    'f8': 'G7',
    'f9': 'G#7',
    'f10': 'A7',
    'f11': 'A#7',
    'f12': 'B7',
    'print screen': 'C8',
    'scroll lock': 'A#1',
    'insert': 'B1',
    'home': 'C2',
    'page up': 'C#2',
    'delete': 'D2',
    'end': 'D#2',
    'page down': 'E2',
    'up': 'F2',
    'left': 'F#2',
    'down': 'G2',
    'right': 'G#2',
    'num 0': 'A2',
    'decimal': 'C5',
    'num 1': 'C#5',
    'num 2': 'D5',
    'num 3': 'D#5',
    'num 4': 'E5',
    'num 5': 'F5',
    'num 6': 'F#5',
    'num 7': 'G5',
    'num 8': 'G#5',
    'num 9': 'A5',
    'num /': 'A#5',
    '*': 'B5',
    'num -': 'C6',
    'plus': 'C#6',
    'enter2': 'D6'
}

reverse_key_settings = {j: i for i, j in key_settings.items()}

# switching mode for self playing ('self'),
# or play midi ('show'),
# or play chords with self-configured playing chords keys settings ('chord')
mode = 'show'
self_device = 'pc'
midi_device_id = 1

# operation key settings for pause, unpause, repeat and so on
pause_key = 'space'
repeat_key = 'ctrl'
unpause_key = 'enter'
exit_key = 'esc'
pause_key_clear_notes = False

# show_key set to True will show what keyboard keys you are pressing
show_key = False

# if mode is 'show', you can set musicsheet as a musicpy sentence,
# or set the path of midi you want to play
musicsheet = "(chd('C','maj7').set(4,1))*3"

path = None

# these are the number of tracks of the midi you want to play from
track_ind = 2
track = 1

# the bpm you want to play
bpm = None

# play_interval: play the parts of the midi in this interval (percentages)
play_interval = None

# these are the init parameters of the mixer
frequency = 44100
size = -16
channel = 1
buffer = 1024
maxinum_channels = 100

global_volume = 0.6

# if delay is set to True, when you are self playing, the sounds will
# last for delay_time seconds
delay = True
delay_time = 3

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
sound_format = 'wav'

# the path of the sounds folder
sound_path = 'sounds/'

# when the mode is in 'show' mode, the delay time for the sounds
show_delay_time = 1

# these are the parameters for chord types detections
# ignore_sort_from : avoid the detection result are sorting from another chord as much as possible
# change_from_first: detection result is preferentially chosen as changed from another chord(flat or sharp some notes)
# original_first: detection result is preferentially chosen as a variation of the original position of the chord(i.e. no inversion or any changes to the notes of the chord)
# ignore_add_from : detection result will ignore the result for adding notes from another chord
detect_mode = 'chord'
inv_num = False
rootpitch = 5
ignore_sort_from = False
change_from_first = True
original_first = True
ignore_add_from = True
same_note_special = False
whole_detect = True
return_fromchord = False
two_show_interval = True
poly_chord_first = False
root_position_return_first = True

# the operations on the midi you want to play
# show_change_pitch : a positive number: will sharp all the notes in the midi by the number; a negative number: same except flat all the notes
# show_modulation : [scale1, scale2] perform modulation from scale1 to scale2 on the notes in the midi
show_change_pitch = None
show_modulation = None

# if this is set to True, then you enable the config key during the playing
config_enable = True

# if you press the config key with the following keys, those keys will be able to adjust settings in realtime.
config_key = 'alt'

# volume change keys
volume_up = '='
volume_down = '-'

# volume change of each volume up/down
volume_change_unit = 0.05

# if delay is set to True before you press, then it will change to False, if False before then set to True
change_delay = 'd'
change_read_current = 'c'
change_pause_key_clear_notes = 'x'

# chords types for each key if you use 'chord' mode
# During the chord mode, if you press a root note key with a chord key,
# then the piano will play that chord types with the root note,
# you can set some keys for chord inversions (i.e. 1st inversion, 2nd inversion, ...),
# and you can even set keys for reversing a chord, and the tempo and interval of the
# chord could also be setted and changed.
CHORDKEY = {
    'num 0': 'maj',
    'decimal': 'm',
    'num 1': '7',
    'num 2': 'maj7',
    'num 3': 'm7',
    'num 4': 'dim7',
    'num 5': 'o7',
    'num 6': 'aug',
    'num 7': 'fifth 9th',
    'num 8': '5(+octave)',
    'num 9': 'mM7'
}

# keys for chord inversions and reversing
CHORD_MODIFY = {
    'f1': [1, 'inv'],
    'f2': [2, 'inv'],
    'f3': [3, 'inv'],
    'f4': [4, 'inv'],
    'f5': [0, 'reverse'],
    'f6': [1, 'inv_high']
}

# chords' intervals and durations (timing unit: miliseconds)
chord_interval = 0.3
chord_duration = 1
note_place = [(-5.0, 50), (10, 102), (19.6, 50), (44.2, 50), (59.0, 102),
              (68.80000000000001, 50), (83.6, 102), (93.4, 50), (118.0, 50),
              (132.8, 102), (142.60000000000002, 50), (157.4, 102),
              (167.20000000000002, 50), (182.0, 102), (191.8, 50), (216.4, 50),
              (231.20000000000002, 102), (241.0, 50), (255.8, 102),
              (265.6, 50), (290.20000000000005, 50), (305.0, 102), (314.8, 50),
              (329.6,
               102), (339.40000000000003, 50), (354.20000000000005, 102),
              (364.0, 50), (388.6, 50), (403.40000000000003, 102),
              (413.20000000000005, 50), (428.00000000000006, 102), (437.8, 50),
              (462.40000000000003, 50), (477.20000000000005, 102), (487.0, 50),
              (501.80000000000007, 102), (511.6, 50), (526.4000000000001, 102),
              (536.2, 50), (560.8000000000001, 50), (575.6, 102),
              (585.4000000000001, 50), (600.2, 102), (610.0, 50), (634.6, 50),
              (649.4000000000001, 102), (659.2, 50), (674.0, 102),
              (683.8000000000001, 50), (698.6, 102), (708.4000000000001, 50),
              (733.0, 50), (747.8000000000001, 102), (757.6, 50),
              (772.4000000000001, 102), (782.2, 50), (806.8000000000001, 50),
              (821.6000000000001, 102), (831.4000000000001, 50), (846.2, 102),
              (856.0, 50), (870.8000000000001, 102), (880.6, 50), (905.2, 50),
              (920.0000000000001, 102), (929.8000000000001, 50),
              (944.6000000000001, 102), (954.4000000000001, 50), (979.0, 50),
              (993.8000000000002, 102),
              (1003.6, 50), (1018.4000000000001, 102), (1028.2, 50),
              (1043.0, 102), (1052.8, 50), (1077.4, 50), (1092.2, 102),
              (1102.0, 50), (1116.8, 102), (1126.6000000000001, 50),
              (1151.2, 50), (1166.0, 102), (1175.8000000000002, 50),
              (1190.6000000000001, 102), (1200.4, 50), (1215.2, 102),
              (1225.0, 50), (1249.6000000000001, 50)]

# load sounds from the folders of sound paths when playing or not
load_sound = True

# detect chord types when the current notes change
show_chord = True

# names of intervals
perfect_unison = 0
minor_second = 1
augmented_unison = 1
major_second = 2
diminished_third = 2
minor_third = 3
augmented_second = 3
major_third = 4
diminished_fourth = 4
perfect_fourth = 5
augmented_third = 5
diminished_fifth = 6
augmented_fourth = 6
perfect_fifth = 7
diminished_sixth = 7
minor_sixth = 8
augmented_fifth = 8
major_sixth = 9
diminished_seventh = 9
minor_seventh = 10
augmented_sixth = 10
major_seventh = 11
diminished_octave = 11
perfect_octave = 12
octave = 12
augmented_seventh = 12

# the parameters of the function split_melody
melody_tol = minor_seventh
chord_tol = major_sixth

# notes showing mode: choose one from 'dots' and 'bars' and 'bars drop',
# or you can set as other names, and turn on the draw piano keys mode
note_mode = 'bars drop'
bar_width = 14
bar_height = 20
bar_color = (124, 252, 0)
bar_y = 174
bar_offset_x = 6
bar_opacity = 160
opacity_change_by_velocity = True
# color mode: choose one from 'normal' and 'rainbow'
color_mode = 'normal'
bar_steps = 6
bar_unit = 50
bar_hold_increase = 5
bars_drop_interval = 2
bars_drop_place = 173
adjust_ratio = 55

# when play midi files, if you choose to merge all tracks, get_off_drums
# set to True will not merge the drum tracks if your midi file has
get_off_drums = True

sort_invisible = False

play_as_midi = False

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

piano_background_image = 'piano_background.png'
