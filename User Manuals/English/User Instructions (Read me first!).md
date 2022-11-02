# User Instructions


## How to modify the configuration parameters?

The various parameters of this software can be modified by clicking `SETTINGS` button on the main screen to open change settings window, save it and then close the change settings window, the changes will take place immediately.

To see what each configuration parameter means, you can see the settings manual.



## How to change the background image?

The easiest way is to directly drag and drop local image files onto the main window to change the background image. You can also directly drag and drop MIDI files onto the main window to load MIDI files, instead of clicking the play MIDI button. (drag and drop functionality is currently not supported for macOS)

Other way: Change the parameter `background_image` in the settings file to the path of the background image you want to set, save it and reopen Ideal Piano. For other parameters, please refer to the setup manual.

You can adjust the transparency of background image by setting the config parameter `background_opacity` from 0 to 255 (transparent to non-transparent).



## What do the buttons on the main screen do?

* click the `PLAY` button to enter the computer keyboard playing mode
* click the `MIDI KEYBOARD` button to enter the MIDI keyboard playing mode
* right click `MIDI KEYBOARD` button to open the choose MIDI device window
* click `PLAY MIDI` button to enter the MIDI file playing mode
* when entering one of these modes, click `GO BACK` button to go back to the initial page
* click `SETTINGS` button to open the change settings window



## When playing MIDI files, how do I pause, unpause and play again?

When you are playing a MIDI file in Ideal Piano, by default you can press `space` on the computer keyboard to pause playing, press `enter` to continue playing. After current playing is finished, by default you can press `ctrl` to play again. All of these key settings can be customized in the config file, please look at the settings manual.



## Why can't I hear any sound when playing MIDI files?

This problem occurs usually when the current MIDI output port cannot produce sound, you can right click the `MIDI KEYBOARD` button to open the window of selecting MIDI device, select the MIDI output port that can be used in the MIDI output driver box, then close the window and try to play the MIDI file again.



## How do I show the corresponding note names on piano keys?

Change the parameter `show_note_name_on_piano_key` to `True` to display the corresponding note names on piano keys. The default is to show the note name of each white key, you can also change `show_only_start_note_name` to `True` to show only the keys with C as the note name.



## How do I display the details of current chord?

Ideal Piano can display detailed information about the chord that is currently playing, including the root note, chord type, inversions, omissions, altered notes, voicings, etc. Change the parameter `show_chord_details` to `True` to display the details of the chord that is currently playing.



## How do I display the key that is currently playing?

Change `show_current_detect_key` to `True` to display the key that is currently playing. There are currently 3 key analysis algorithms to choose from, set the value of `current_detect_key_algorithm` to 0, 1, or 2. The default 3rd algorithm is suitable for analyzing MIDI files with modulations. This algorithm analyzes the whole piece before displaying it, so it cannot be used for real-time performance. If you want to display current key while playing in real time, you can choose the 1st and 2nd algorithm to determine the keys. Both algorithms analyze the keys in real time, but are not as accurate as the 3rd algorithm.

By default, the key detection algorithm only detects major or minor keys, change `current_detect_key_major_minor_preference` to `True` to include detections for church modes like dorian, lydian.



## Is there a compatible version for Linux and macOS?

There are Linux and macOS compatible versions, you can download at the [release page](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest) of Ideal Piano on github. For the installation of Linux and macOS versions, here are the instructions.

### Linux

You can download the Linux compatible version from the release page, which contains the Linux executable for Ideal Piano, double click to open the software to use.

For Linux version,  playing MIDI files using default settings requires installing freepats, which is the default MIDI sound set that pygame's mixer music module uses to play MIDI files. On Ubuntu you can run

```
sudo apt-get install freepats
```

If you want to use SoundFont files as instruments in the Linux version, you need to install fluidsynth, you can refer to [here](https://github.com/FluidSynth/fluidsynth/wiki/Download) for the install command for different Linux distributions. For Ubuntu, it is

```
sudo apt-get install fluidsynth
```

### macOS

You can download the macOS compatible version from the release page, which contains the macOS app for Ideal Piano, double click to open the software to use.

Note: currently pygame's mixer has a bug that it cannot pause MIDI file playing on macOS, which is used by default to play MIDI files in Ideal Piano, this bug only appears on macOS, for Windows and Linux the pause function works fine. So by default the pause function in the playing MIDI files mode will not work, if you want to pause and unpause MIDI file playing in Ideal Piano macOS version before pygame's developers fix this bug, you can switch to use fluidsynth to play MIDI files in Ideal Piano by changing `use_soundfont` to True in the settings file. Then you need to install fluidsynth on macOS, which is pretty easy, you can use homebrew to install fluidsynth. You can run this line in the terminal to install fluidsynth using homebrew.

```
brew install fluidsynth
```



## The text display is weird or I don't like the fonts, can I change it?

Yes, you can, please refer to the settings manual, to be short, you can change the setting parameter `fonts` in the settings file to the font you like, note that the font should be already installed in your computer.




## Why can't Ideal Piano detect my MIDI keyboard?

The most possible case is that the current MIDI device id in Ideal Piano does not match with your MIDI keyboard. In this case, you can right click on `MIDI KEYBOARD` button to open the choose MIDI device window to choose current MIDI device as your MIDI keyboard, you should choose the MIDI device in MIDI Input Driver box to make this works.

For the other cases, if you open the DAW, the MIDI keyboard is already available in the DAW, then Ideal Piano can't detect your MIDI keyboard at this time, because a MIDI keyboard can only control one software at most, so at this time the DAW has already occupied the MIDI keyboard, and Ideal Piano can't detect the MIDI keyboard.

If you want to use a MIDI keyboard in a DAW and also use Ideal Piano, there is a very simple solution.

Using loopMIDI, a free software, you can use both DAW and Ideal Piano to play MIDI keyboard, the procedure is as follows.



## How to use Ideal Piano with DAW?

### Using a MIDI keyboard in the DAW

Previously I wanted to implement a MIDI keyboard shared by both DAW and Ideal Piano, or to play a project in DAW and display the current notes in Ideal Piano, but at the beginning it failed, always showing errors like Host error, but later I found a good solution. loopMIDI is a free software that allows you to create virtual MIDI ports, so you can use it to connect to the MIDI ports of several different software. With loopMIDI you can use a MIDI keyboard for both the DAW and Ideal Piano, so you can load the source you want to hear in the DAW and then play it on the MIDI keyboard and hear the DAW source, while Ideal Piano can display the chord type and notes you are currently playing in real time.

The download link of loopMIDI: [click here](https://www.tobias-erichsen.de/software/loopmidi.html)

With loopMIDI, a free software, you can play with a MIDI keyboard in the DAW, and at the same time Ideal Piano can display the current notes and the corresponding chords, so you can listen to the instrument you want more easily and see what you are playing in Ideal Piano.

Take FL Studio for example, first open loopMIDI, create a new MIDI port, (click on the + sign below) and then open FL Studio, in the MIDI settings in the options, select the MIDI keyboard you are connected to on the input side, and select the new MIDI port you just created on the output side.

The input MIDI keyboard should be enabled, the port should not be set (left blank), and the output MIDI port should be set with a port number, for example 0.

Then load an instrument sound source and set the MIDI output port number for this instrument to the same number as the output MIDI port.

Then open Ideal Piano, change `midi_device_id` in the config.py file to the number of the new MIDI port in loopMIDI, and remember to set the parameter load_sound to False, so that Ideal Piano will not load the sound source you set, and will only play the sound source in the host when you play it. so that Ideal Piano will not load the sources it has set up, and will only play the sources from the host when playing.

For some sources, even if the MIDI output port is set to the same loopMIDI as the host, the solution is to use the MIDI out plugin, set the port to the same MIDI output port as the host, then set the input port of the source to the MIDI out port, and select the MIDI out channel to play when you play to receive the data. (Another important point is that

(There is also a very important point is that you must first import the source, and then import the MIDI out plug-in, and then set the port, every time you change the new source to this order, otherwise the data still can not pass loopMIDI)

### Play the project in the DAW

With loopMIDI you can also play the project in the DAW and at the same time Ideal Piano can demonstrate the current notes and chords, you just need to set the MIDI out port of the DAW and the MIDI out port of the source to the same number, which corresponds to the new MIDI port you created in loopMIDI.

For example, if loopMIDI creates a new MIDI port called MIDI port A, then in the MIDI settings of the DAW, set the port corresponding to MIDI port A to 0, then set the MIDI output port of the audio source to 0 as well, and then set the setting parameter `midi_device_id` to the number corresponding to MIDI port A.

Then click the MIDI keyboard button to enter MIDI keyboard mode, at this time, play the track with the MIDI output port set in the DAW. When you play the track with the MIDI output port, you can see that Ideal Piano also follows the same notes in real time.

For some sources that are set up with MIDI out but still can't pass data to loopMIDI, the solution is also to use MIDI out as a relay station, but this is slightly different from playing with a MIDI keyboard.

When playing with a MIDI keyboard, you can select the MIDI out track to play, and the sound will come from the source paired with the MIDI port, and Ideal Piano can also receive the MIDI signal, but if you don't use the MIDI keyboard and play the project directly in the DAW, you can't transfer the data to loopMIDI even if you select the MIDI out track to play. I found a solution to this problem by copying the pairing and playing the track.

The solution I found was to copy the notes from the track of the source paired with the MIDI port to the piano window of MIDI out, then mute the track of that source and let MIDI out play only, then I could hear the sound of the track of the source when it was not muted before, and I could also transfer data to loopMIDI, so Ideal Piano could also can receive the MIDI signal in real time.



## Other cautions of choose MIDI files window

The MIDI track box can be left blank, and the program I wrote will intelligently find the first track with notes in the MIDI file you choose and use it as the track to play. So if it is a pure piano piece with only one track, then you can leave it blank and the program will play the track with the notes directly, if it is a MIDI with multiple tracks, then you can fill in the track you want to play according to your needs.

In this mode, the selected MIDI file will be played in Ideal Piano, with the sound coming from a built-in General MIDI player by default. You can change `play_as_midi` in the settings file to `False` to make the sound coming from the sound source you set. The sound source must be a folder with audio files named after notes, like `C5.wav`. The current position of the notes on the piano will be displayed on the screen, and the chords of the notes currently played will be analyzed in real time.



## What do I need to pay attention to when loading audio files as sound source?

You can set the path of the sound source when you play the piano, the parameter is `sound_path`, and the format of the sound file should be unified, the parameter of the sound file format is `sound_format` (such as wav, mp3, ogg, etc.). Note that the parameters here are limited to audio files as sound sources.



## How to load SoundFont files as sound source?

To load a SoundFont file as a source for playing MIDI files, please set `use_soundfont` to True and `play_as_midi` to True in the settings file, and set the path to the SoundFont file via `sf2_path`.

Please set `play_use_soundfont` in the setup file to True, and you can customize the instruments in the SoundFont file as well as the duration of the notes played, the volume, etc. with a series of parameters such as `bank`, `preset`, etc. etc.

Use `Ctrl + S` to open the change settings page, and `Ctrl + R` to reload the modified parameters. If you click the `save` button on the page where you modified the settings or press `Ctrl + S` to save the settings, the settings will be automatically reloaded after the page where you modified the settings is closed.

If you are playing with SoundFont, you can use key combinations to change the preset number and bank number to change the instrument while playing:

`Ctrl + 1` (previous preset)

`Ctrl + 2` (next preset)

`Ctrl + 3` (previous bank)

`Ctrl + 4` (next bank)



## I have encountered other problems or have suggestions for improvement

If you have encountered any problems and need help or have any feedback, please email me at [2180502841@qq.com](mailto:2180502841@qq.com) or add my qq number 2180502841 to talk to me, thanks for your support~

