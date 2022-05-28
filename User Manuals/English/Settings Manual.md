# Settings Manual

Here we give you an explanation of what each parameter in the configuration file config.py corresponds to, so that you can be clearer when you modify it.

## Contents

- [Screen related parameters](#screen related parameters)
- [Pygame mixer initialization parameters](#pygame mixer initialization parameters)
- [Keyboard playing and MIDI files playing parameters](#keyboard playing and MIDI files playing parameters)
- [Chord analysis parameters](#chord analysis parameters)
- [Parameters of the algorithm for separating the main melody of a piece](#parameters of the algorithm for separating the main melody of a piece)
- [Note display related parameters](#note display related parameters)
- [Piano keyboard related parameters](#piano keyboard related parameters)
- [SoundFont file related parameters](#soundFont file related parameters)
- [Show composition analysis](#show composition analysis)
  - [Related parameters](#related parameters)

## Screen related parameters

screen_size: screen size (width, height)

background_image: background image file path

background_size: background image size

piano_image: piano image file path

piano_size: piano image size

message_color: font color for chord display, formatted as (R, G, B, A)

fonts_size: font size

label1_place: text position of the currently played note name

label2_place: text position of the chord name

label3_place: text position of the status of the MIDI file being played

label_anchor_x: horizontal alignment of the text

label_anchor_y: vertical alignment of the text

fonts: font name

bold: whether to bold the text

go_back_image: Returns the button's image file path

go_back_place: Returns the image location of the button

self_play_image: the image file path of the computer keyboard's play button

self_play_place: The location of the computer keyboard play button image

self_midi_image: the image file path of the midi keyboard play button

self_midi_place: The location of the midi keyboard play button image

play_midi_image: the image file path of the play MIDI file button

play_midi_place: the image location of the play MIDI file button

key_settings: The dictionary of the 88 keys of the computer keyboard, please note that all the files in the sound path must contain the keys you have set to

midi_device_id: This parameter is the id of the midi device after it is connected to the midi device (e.g. midi keyboard)

language: the display language of the software, including main window buttons, chord names, messages and the window to choose MIDI files, currently only 'English' and 'Chinese' are supported

## pygame mixer initialization parameters

frequency, size, channel, buffer, max_num_channels

(please refer to pygame's mixer module documentation online)

## Keyboard playing and MIDI files playing parameters

pause_key: key to pause

repeat_key: key to repeat playback

unpause_key: key to continue (while paused)

global_volume: total volume, max 1, min 0

delay: whether to give a certain delay to the tone after it is released

delay_time: the delay time (in seconds)

fadeout_ms: the time in milliseconds to fade out after the note is played

touch_interval: the interval between the end of a note and its replay when the same note is played continuously, in seconds

pause_key_clear_notes: whether to clear the display of all currently played notes when pausing

delay_only_read_current: When a note is delayed (not pressed), the chord judgment does not include those notes that are still delayed, only those that are currently pressed

sound_format: the file format of the sound source (file extension)

sound_path: the file path of the sound source

show_delay_time: the delay time of the notes when playing the MIDI file

config_enable: whether to enable function keys when playing on computer keyboard

config_key: the key position of the function keys, the function keys can be used with other keys to do different functions

volume_up: the key to use with the function keys to raise the total volume

volume_down: the key that is used with the function key to lower the volume

volume_change_unit: the volume of the total volume that changes each time

change_delay: The key used with the function key to change the delay or not

change_read_current: The key used with the function key to change whether only the currently pressed chord is judged

change_pause_key_clear_notes: key used with function keys to change whether the display of the currently played note is cleared when paused

note_place: The position of all keys on the piano from left to right in note point mode

load_sound: whether to load the sound source and play it when playing (set to False when using with the host)

show_key: whether to show the name of the keys of the computer keyboard when playing on it

show_chord: Whether or not the chord is analyzed in real time by musical logic

show_notes: whether to show the current notes in real time when playing

get_off_drums: If True, in midi playback mode, if you choose to merge all tracks, the drum tracks will be removed after the MIDI file is read (if any) to avoid the demo chords being scrambled by the drum notes.

sort_invisible: if True, the sorted content will not be shown in the display chords (e.g. `Fmaj7 sort as [2,3,1,4]` will become `Fmaj7`)

play_as_midi: When playing a MIDI file, the software uses the SoundFont file that comes with Ideal Piano to play the MIDI file. The advantage is that MIDI files with a lot of notes will load much faster and do not lag when playing a lot of notes and complex chord types at the same time. Set to True to enter this mode. You can also change the SoundFont file used for playback by changing `sf2_path`.

pitch_range: A tuple of two pitch strings, which filters out the notes between them when reading a MIDI file, to prevent the notes from exceeding the pitch range set by the piano.

soft_pedal_volume: The ratio of the reduction of the volume of the notes when the weak pedal is pressed in MIDI keyboard playing mode, a decimal number between 0 and 1

## Chord analysis parameters

These are the parameters of the chord logic algorithm, the default settings are the most widely used, so if I want to explain what they mean, I may need to understand my algorithm first, so I will explain this part later when I introduce it

inv_num = False

change_from_first = True

original_first = True

same_note_special = False

whole_detect = True (changing this parameter to `False` will improve the speed of real-time analysis, but very complex chords may not be analyzed)

return_from_chord = False

poly_chord_first = False

root_position_return_first = True

alter_notes_show_degree = True

## Parameters of the algorithm for separating the main melody of a piece

melody_tol, chord_tol, get_off_overlap_notes, average_degree_length, melody_degree_tol

## Note display related parameters

note_mode: Select the note display mode, currently there are 2 modes to choose from: note bars rising and note bars falling (only available in MIDI file mode), corresponding to 'bars' and 'bars drop' respectively

bar_width: the width of the note bar

bar_height: the length of the note bar

bar_color: the color of the bar, RGB tuple

sustain_bar_color: the color of the bar when the key is released while the piano pedal is pressed in MIDI keyboard play mode, RGB tuple

bar_y: the vertical coordinate of the bar's appearance

bar_offset_x: the pixel value of the horizontal coordinate of the note bar that deviates from the note point

bar_opacity: the transparency of the note bar, from 0 to 255, from fully transparent to fully opaque

opacity_change_by_velocity: if or not the transparency of the bar changes according to the keypress force, the lighter the keypress force, the more transparent the bar is, the heavier the keypress force, the more opaque the bar is

color_mode: the color mode of the note bar, currently there are two modes to choose from, monochrome and random, corresponding to 'normal' and 'rainbow' respectively (actually, you can fill in other text that is not normal)

bar_steps: the number of pixels the note bar moves each time it rises

bar_unit: the length of the note bar in units for calculating the relative length when playing MIDI files

bar_hold_increase: The number of pixels that the note bar lengthens each time a key is held down (or a computer key is held down)

bars_drop_interval: in note bar (drop) mode, how long it takes for the bar to drop from the top of the screen to the specified position, in seconds

bars_drop_place: the specified position (height) that the note bar will drop to in note drop mode

adjust_ratio: A parameter that adjusts the accuracy of the bar drop to the specified position, generally not needed

use_track_colors: whether to use different colors on different tracks and instruments

tracks_colors: list of colors for different tracks and instruments, RGB parameter

use_default_tracks_colors: whether to use set track colors or use randomly generated colors for different tracks

bar_border: the width of the bar's border

bar_border_color: the border color of the note bar, it is the RGB tuple, `(R, G, B)`.

## Piano keyboard related parameters

draw_piano_keys: set to True to enter the draw piano mode, (according to the parameters and the structure of the piano 88 keys to draw the piano keyboard, replacing the previous piano picture) In the draw piano mode, the corresponding keys will light up when the midi keyboard is played or the computer keyboard is played, including when the MIDI file is played in drop note mode, the notes will also light up when they land on the keys. The piano is drawn using black and white keys that directly follow the structure of the piano's 88 keys, according to settable parameters, and each key can change color. Underneath the drawing of the 88 keys there is a black background image, which is mainly used to show the gaps between the piano keys (for filling). You can turn off note mode (note_mode can be set to a value other than bars, bars drop) and just turn on draw piano mode, the corresponding piano key will be lit up when playing and the current note will be lit up when playing the MIDI file. It is also possible to use any of the note modes and turn on draw piano mode.

white_key_width: the width of the piano's white keys (horizontal length)

white_key_height: the height of the piano's white keys (vertical length)

white_key_interval: the distance between every two white keys of the piano

white_key_y: the height position of the piano's white keys

white_keys_number: the number of white keys of the piano

white_key_start_x: the horizontal position of the first white key of the piano

white_key_color: the color of the piano's white keys

black_key_width: the width (horizontal length) of the piano's black keys

black_key_height: the height of the piano's black key (vertical length)

black_key_y: the height position of the piano's black key

black_key_first_x: horizontal position of the first black key of the piano

black_key_start_x: horizontal position of the second black key of the piano

black_key_color: the color of the piano's black keys

black_keys_set: the relative interval between each black key in each group, except for the first black key, which is set individually, in groups of 5 (the first interval is usually 0, which means that the first black key starts from the leftmost relative position in the current group)

black_keys_set_interval: the interval between every two black keysets

black_keys_set_num: the number of black keysets

piano_background_image: the background image under the piano (to fill the gap)

piano_key_border: the width of the piano's keyboard border

piano_key_border_color: piano_key_border_color, RGB tuple, `(R, G, B)`

## SoundFont file related parameters

use_soundfont: Whether to use SoundFont files to play MIDI files, when this is set to True, rendering the MIDI file to be played to audio with the loaded SoundFont file to play when playing the MIDI file

play_use_soundfont: Whether to use the SoundFont file when playing on a computer keyboard or a MIDI keyboard

sf2_path: The path of the SoundFont file

bank: the bank number of the SoundFont file

preset: the preset number of the SoundFont file

sf2_duration: the length of the notes generated by the SoundFont file, in seconds

sf2_decay: the fade-out time of the notes generated by the SoundFont file, in seconds

sf2_volume: the volume of the note generated by the SoundFont file, in units of MIDI note velocity

sf2_path: path to the SoundFont file

render_as_audio: this parameter is useful for Linux version, since fluidsynth installed by apt or other package manager on some Linux system is not recent version, and the pause and unpause functionality when using fluidsynth as MIDI player may not work properly in this case, when this parameter is set to True, use the rendered audio as playback, if it is set to False, use fluidsynth as the MIDI player

## Show composition analysis

Ideal Piano can read a text file with a composition analysis in a specific format, and display the composition techniques such as modulation, subordinate chords, borrowed chords, etc. in the demo MIDI file mode according to the number of bars in the current composition. The default file is musical analysis.txt.

The format of the composition analysis file is

Number of bars1

Composition analysis content1



Number of bars 2

Composition analysis content 2



Number of bars 3

Composition Analysis 3

...

The number of bars here starts with bar 1, and the number of bars is a number, either an integer or a decimal. The composition analysis content is the content you want to display when you reach the specified number of bars. The software will parse the composition analysis file format and find the position of the first note up to the current number of bars, and then display the corresponding composition content when it reaches the corresponding note position during the demo.

Currently, in addition to this format, it also supports displaying the tonicity, so that you can display the current tonicity at any position, and if the piece has a modulation, you can write the tonicity statement before the beginning bar of the modulation. The syntax is (here is an example)

key: Tone 1 (you can write anything you want here, such as A major, A major, etc.)



Number of bars 1

Composition analysis content 1



Number of bars 2

Composition analysis content 2



Number of bars 3

Composition analysis 3



key: key 2 (you can write a new key when the piece is modulated)



Number of bars n

Composition analysis content n



Number of bars x

Composition analysis content x



Number of bars y

Composition analysis content y

...

(The phrase indicating the tonality must be separated from the measure statement by one line, and a measure statement must be adjacent to the corresponding composition analysis statement on the top and bottom of the line, together called a measure block. (Multiple lines can be written within a composition analysis statement, but there must not be a completely empty line in between)

(The number of bars supports both absolute bar position and relative bar position syntax, absolute bar position is a number, which can be an integer or a decimal, relative bar position syntax is + relative bar length, for example, +1 means the position of the next bar relative to the previous position, +1/2 means the position of the next one-half bar relative to the previous position, relative bar position supports integers, decimals and fractions.)



In order to be able to quickly input a large number of compositional analysis statements, especially when analyzing a piece with complex chord progressions, I myself generally write the latest 4-5 chords and divide them into 4-5 bar blocks, putting an arrow in front of the chord when each bar block reaches one of the chords, with different compositional techniques explained below, such as

+1

Emaj9(omit 3) | D#m7 | DM7 | → C#11(omit 3)

IVM9 iii7 bIIIM7 V11 (F# major)

You can use the editor of [music_analysis_batch_language](https://github.com/Rainbow-Dreamer/music_analysis_batch_language) to generate music theory analysis statements according to the batch syntax of README .

Using this batch syntax I designed, you can input a large number of music analysis statements very concisely and quickly, and the syntax of the music analysis statements itself is very comfortable for non-programmers to read directly. So you can also use this special batch statement as a small programming language to write chord function analysis, I think it's still very good :D

### Related parameters

show_music_analysis: whether to turn on the display of the composition analysis

music_analysis_file: the file path of the composition analysis file to read

music_analysis_place: set the position of the composition content to be displayed

key_header: the beginning of the key (this parameter shows the beginning of the key, e.g. "current key:")

music_analysis_width: the width of the music analysis text label

music_analysis_fonts_size: the font size of the music analysis text

