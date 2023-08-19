# User Instructions



## Contents

* [How to modify the configuration parameters?](#how-to-modify-the-configuration-parameters)
* [How to change the background image?](#how-to-change-the-background-image)
* [What do the buttons on the main screen do?](#what-do-the-buttons-on-the-main-screen-do)
* [When playing MIDI files, how do I pause, unpause and play again?](#when-playing-midi-files-how-do-i-pause-unpause-and-play-again)
* [Why can't I hear any sound when playing MIDI files?](#why-cant-i-hear-any-sound-when-playing-midi-files)
* [How do I show the corresponding note names on piano keys?](#how-do-i-show-the-corresponding-note-names-on-piano-keys)
* [How do I display the details of current chord?](#how-do-i-display-the-details-of-current-chord)
* [How do I display the key that is currently playing?](#how-do-i-display-the-key-that-is-currently-playing)
* [Is there a compatible version for Linux and macOS?](#is-there-a-compatible-version-for-linux-and-macos)
* [How to build from instrument?](#how-to-build-from-instrument)
* [The text display is weird or I don't like the fonts, can I change it?](#the-text-display-is-weird-or-i-dont-like-the-fonts-can-i-change-it)
* [When playing MIDI files, the sound is not synchronized with when the bars hitting on piano keys?](#when-playing-midi-files-the-sound-is-not-synchronized-with-when-the-bars-hitting-on-piano-keys)
* [Why can't Ideal Piano detect my MIDI keyboard?](#why-cant-ideal-piano-detect-my-midi-keyboard)
* [How to use Ideal Piano with DAW?](#how-to-use-ideal-piano-with-daw)
* [What do I need to pay attention to when loading audio files as instrument?](#what-do-i-need-to-pay-attention-to-when-loading-audio-files-as-instrument)
* [How to load SoundFont files as instrument?](#how-to-load-soundfont-files-as-instrument)
* [I have encountered other problems or have suggestions for improvement](#i-have-encountered-other-problems-or-have-suggestions-for-improvement)



## How to modify the configuration parameters?

The various parameters of this software can be modified by clicking `SETTINGS` button on the main screen to open change settings window, save it and then close the change settings window, the changes will take place immediately. Or you can use `Ctrl + S` to open the change settings page, and `Ctrl + R` to reload the modified parameters. If you click the `save` button on the page where you modified the settings or press `Ctrl + S` to save the settings, the settings will be automatically reloaded after the page where you modified the settings is closed.

To see what each configuration parameter means, you can see the settings manual.



## How to change the background image?

The easiest way is to directly drag and drop local image files onto the main window to change the background image. You can also directly drag and drop MIDI files onto the main window to load MIDI files, instead of clicking the play MIDI button. (drag and drop functionality is currently not supported for macOS)

Other way: Change the settings parameter `background_image` to the path of the background image you want to set, save it and reopen Ideal Piano. For other parameters, please refer to the setup manual.

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

By default, the key detection algorithm only detects major or minor keys, change `current_detect_key_major_minor_preference` to `False` to include detections for church modes like dorian, lydian.



## Is there a compatible version for Linux and macOS?

There are Linux and macOS compatible versions, you can download from [here](https://www.jianguoyun.com/p/Daurwu0QhPG0CBjxt8QEIAA). For the installation of Linux and macOS versions, here are the instructions.

### Linux

You can download the Linux compatible version from the provided link above, which contains the Linux executable for Ideal Piano, double click to open the software to use.

For Linux version,  to play MIDI files using the default settings you need to make sure that you currently have a MIDI output port that can produce sound, and then select the corresponding MIDI output port in the Choose MIDI Device window. Here is a recommendation to install freepats and timidity. On Ubuntu you can run

```
sudo apt-get install freepats timidity
```

Then open terminal, run `timidity -iA` to open the MIDI port of timidity, and then select the MIDI output port of timidity in the Choose MIDI Device window.

If you want to use SoundFont files as instruments in the Linux version, you need to install fluidsynth, you can refer to [here](https://github.com/FluidSynth/fluidsynth/wiki/Download) for the install command for different Linux distributions. For Ubuntu, it is

```
sudo apt-get install fluidsynth
```

### macOS

You can download the macOS compatible version from the provided link above, which contains the macOS app for Ideal Piano, double click to open the software to use.

For macOS version,  to play MIDI files using the default settings you need to make sure that you currently have a MIDI output port that can produce sound, and then select the corresponding MIDI output port in the Choose MIDI Device window.

If you don't currently have any MIDI ports with a synthesizer, here's a suggestion to install VMPK (Virtual MIDI Piano Keyboard), click [here](https://sourceforge.net/projects/vmpk/files/vmpk/0.8.8/vmpk-0.8.8-mac-x64.dmg/download) to download the installation package, open VMPK after installation, open `Edit - MIDI Connections ` from the menu bar, check `Enable MIDI Input` and `Enable MIDI Thru on MIDI Output`, then in the `MIDI IN Driver`, select `CoreMIDI`, then click `OK` to save the settings. Next, right-click on the `MIDI KEYBOARD` button in Ideal Piano to open the interface for selecting MIDI ports, and select `CoreMIDI,MIDI In` in the `MIDI Output Driver` column, close the window. Then you can play MIDI files normally.

You can also use [VMPK](https://sourceforge.net/projects/vmpk/files/vmpk/0.8.8/vmpk-0.8.8-x86_64.AppImage/download) for Linux version, select `ALSA` for `MIDI IN Driver`, and select `ALSA, in` in `MIDI Output Driver` column of the interface for selecting MIDI ports.

If you want to use SoundFont files as instruments in the macOS version, you need to install fluidsynth, it is recommended to install fluidsynth with homebrew.

```
brew install fluidsynth
```



## How to build from instrument?

If you cannot run the executables on your current system, the best solution is to build from instrument code.

Take Linux as an example, the executable build from Ubuntu 21.10 may not work on Ubuntu 22.04 due to some core libraries differences and other incompatible issues with newer versions.

Here are the steps to build Ideal Piano from instrument code. These steps are compatible with Windows, Linux and macOS.

1. Download complete release version from [here](https://www.jianguoyun.com/p/DVCbNrUQhPG0CBjQnvMEIAA), extract the folder `Ideal Piano`.

2. Make sure you have installed python3 in your environment, please don't install the newest version as it may cause incompatible issues with some python library dependencies, the recommended version is python 3.7.9.

3. Use pip to install the following python libraries: `pip install pygame==2.1.2 pyglet==1.5.11 mido_fix pydub py pyqt5 dataclasses pyinstaller`

4. Go to the path `Ideal Piano/packages/`, copy and paste the file `Ideal Piano start program.pyw` to the path `Ideal Piano/`.

5. Then run this code in your IDE to make sure if it works under current environment. You might need to do some more configurations to make it work on some systems or some specific versions. For example, on Ubuntu 22.04, you need to run `sudo apt-get install libxcb-xinerama0` in terminal to make it works.

6. Then modify the line

   ```python
   abs_path = os.path.dirname(os.path.abspath(__file__))
   ```

   to

   ```python
   abs_path = os.path.dirname(sys.executable)
   ```

7. Open terminal in the path `Ideal Piano/`, run `pyinstaller -w -F "Ideal Piano start program.pyw" --hidden-import dataclasses`, wait for the compilation. If you want to add the icon, then add `--icon="reinstruments/piano.ico"` after it. (on macOS the icon file name is `piano_icon.icns`)

8. When the compilation is finished, you can find the executable in the `dist` folder, and move it to the path  `Ideal Piano/` to use it.



## The text display is weird or I don't like the fonts, can I change it?

Yes, you can, please refer to the settings manual, to be short, you can change the setting parameter `fonts` to the font you like, note that the font should be already installed in your computer.



## When playing MIDI files, the sound is not synchronized with when the bars hitting on piano keys?

This issue may occur on computers with less powerful processors. Current configuration parameters works great for the computer it mainly developed on:

CPU: 11th gen Intel(R) Core(TM) i7-11800H

GPU: NVIDIA GeForce RTX 3060 Laptop GPU

RAM: 32GB

You can adjust some settings parameters to make the sound synchronized with the bars.

If the bars fall and hit on piano keys slower or faster than when the sound plays, you can try to adjust the settings parameter `adjust_ratio`, the larger it is, the slower the bar falls.

When you are using multiprocessing mode in playing MIDI files, if the MIDI sound starts playing early or late, you can adjust the settings parameter `play_midi_start_process_time`, which is the time in seconds for initializing the MIDI sound playing process. When you change current playing position, and the bars are out of sync, you can adjust the settings parameter `move_progress_adjust_time`, which is the delay time in seconds when changing the progress bar.




## Why can't Ideal Piano detect my MIDI keyboard?

The most possible case is that the current MIDI input port in Ideal Piano does not match with your MIDI keyboard. In this case, you can right click on `MIDI KEYBOARD` button to open the choose MIDI device window to choose current MIDI device as your MIDI keyboard, you should choose the MIDI device in MIDI Input Driver box to make this works.

For the other cases, if you open the DAW, the MIDI keyboard is already available in the DAW, then Ideal Piano can't detect your MIDI keyboard at this time, because a MIDI keyboard can only control one software at most, so at this time the DAW has already occupied the MIDI keyboard, and Ideal Piano can't detect the MIDI keyboard.

If you want to use a MIDI keyboard in a DAW and also use Ideal Piano, there is a very simple solution.

Using loopMIDI, a free software, you can use both DAW and Ideal Piano to play MIDI keyboard, the procedure is as follows.



## How to use Ideal Piano with DAW?

### Using a MIDI keyboard in the DAW

loopMIDI is a free software that allows you to create virtual MIDI ports, so you can use it to connect to the MIDI ports of several different software. With loopMIDI you can use a MIDI keyboard for both the DAW and Ideal Piano, so you can load the instrument you want to hear in the DAW and then play it on the MIDI keyboard and hear the DAW instrument, while Ideal Piano can display the chord type and notes you are currently playing in real time.

The download link of loopMIDI: [click here](https://www.tobias-erichsen.de/software/loopmidi.html)

With loopMIDI, a free software, you can play with a MIDI keyboard in the DAW, and at the same time Ideal Piano can display the current notes and the corresponding chords, so you can listen to the instrument you want more easily and see what you are playing in Ideal Piano.

Take FL Studio for example, first open loopMIDI, create a new MIDI port, (click on the + sign below) and then open FL Studio, in the MIDI settings in the options, select the MIDI keyboard you are connected to on the input side, and select the new MIDI port you just created on the output side.

The input MIDI keyboard should be enabled, the port should not be set (left blank), and the output MIDI port should be set with a port number, for example 0.

Then load an instrument and set the MIDI output port number for this instrument to the same number as the output MIDI port.

Then open Ideal Piano, change settings parameter `midi_input_port` to the number of the new MIDI port in loopMIDI, and remember to set the settings parameter `load_sound` to False, so that Ideal Piano will not load the instrument you set, and will only play the sound in the DAW when you play it. so that Ideal Piano will not load the instruments it has set up, and will only play the instruments from the DAW when playing.

For some instruments, even if the MIDI output port is set to the same loopMIDI as the DAW, the solution is to use the MIDI out plugin, set the port to the same MIDI output port as the DAW, then set the input port of the instrument to the MIDI out port, and select the MIDI out channel to play when you play to receive the data. (Another important point is that

(There is also a very important point is that you must first import the instrument, and then import the MIDI out plug-in, and then set the port, every time you change the new instrument to this order, otherwise the data still can not pass loopMIDI)

### Play the project in the DAW

With loopMIDI you can also play the project in the DAW and at the same time Ideal Piano can demonstrate the current notes and chords, you just need to set the MIDI out port of the DAW and the MIDI out port of the instrument to the same number, which corresponds to the new MIDI port you created in loopMIDI.

For example, if loopMIDI creates a new MIDI port called MIDI port A, then in the MIDI settings of the DAW, set the port corresponding to MIDI port A to 0, then set the MIDI output port of the instrument to 0 as well, and then set the setting parameter `midi_input_port` to the number corresponding to MIDI port A.

Then click the MIDI keyboard button to enter MIDI keyboard mode, at this time, play the track with the MIDI output port set in the DAW. When you play the track with the MIDI output port, you can see that Ideal Piano also follows the same notes in real time.

For some instruments that are set up with MIDI out but still can't pass data to loopMIDI, the solution is also to use MIDI out as a relay station, but this is slightly different from playing with a MIDI keyboard.

When playing with a MIDI keyboard, you can select the MIDI out track to play, and the sound will come from the instrument paired with the MIDI port, and Ideal Piano can also receive the MIDI signal, but if you don't use the MIDI keyboard and play the project directly in the DAW, you can't transfer the data to loopMIDI even if you select the MIDI out track to play. I found a solution to this problem by copying the pairing and playing the track.

The solution I found was to copy the notes from the track of the instrument paired with the MIDI port to the piano window of MIDI out, then mute the track of that instrument and let MIDI out play only, then I could hear the sound of the track of the instrument when it was not muted before, and I could also transfer data to loopMIDI, so Ideal Piano could also can receive the MIDI signal in real time.



## What do I need to pay attention to when loading audio files as instrument?

You can set the path of the instrument when you play the piano, the parameter is `sound_path`, and the format of the sound file should be unified, the parameter of the sound file format is `sound_format` (such as wav, mp3, ogg, etc.). Note that the parameters here are limited to audio files as instruments.



## How to load SoundFont files as instrument?

To load a SoundFont file as an instrument for playing MIDI files, please set `use_soundfont` to True, and set the path to the SoundFont file via `sf2_path`.

To load a SoundFont files as an instrument for computer keyboard playing and MIDI keyboard playing, please set `play_use_soundfont` to True, and you can customize the instruments in the SoundFont file as well as the duration of the notes played, the volume, etc. with a series of parameters such as `bank`, `preset`, etc. etc.

If you are playing with SoundFont, you can use key combinations to change the preset number and bank number to change the instrument while playing:

`Ctrl + 1` (previous preset)

`Ctrl + 2` (next preset)

`Ctrl + 3` (previous bank)

`Ctrl + 4` (next bank)



## I have encountered other problems or have suggestions for improvement

If you have encountered any problems and need help or have any feedback, please email me at [2180502841@qq.com](mailto:2180502841@qq.com) or add my qq number 2180502841 to talk to me, thanks for your support~

