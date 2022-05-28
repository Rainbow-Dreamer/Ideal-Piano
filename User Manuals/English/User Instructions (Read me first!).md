# User Instructions


## How to modify the configuration parameters?

The various parameters of this software can be modified using `tools/change_settings.exe` or directly to config.py, save it and then open the software to see the changes, or you can press `Ctrl + S` on the computer keyboard to open the page to modify the configuration parameters (`Ctrl` is the default setting key. You can modify the setting key in the configuration parameters, please see the manual for the corresponding parameters).

To see what each configuration parameter means, you can see the settings manual.



## How to change the background image?

The easiest way is to directly drag and drop local image files onto the main window to change the background image. You can also directly drag and drop MIDI files onto the main window to load MIDI files, instead of clicking the play MIDI button. (drag and drop functionality is currently not supported for macOS)

Other way: Change the parameter `background_image` in the settings file to the path of the background image you want to set, save it and reopen Ideal Piano. For other parameters, please refer to the setup manual.



## What do the buttons on the main screen do?

Click the `PLAY` button to enter the computer keyboard playing mode, click the `MIDI KEYBOARD` button to enter the MIDI keyboard playing mode, and click `PLAY MIDI` button to enter the MIDI file playing mode. When entering one of these modes, click `GO BACK` button to go back to the initial page.



## When playing MIDI files, how do I pause, unpause and play again?

When you are playing a MIDI file in Ideal Piano, by default you can press `space` on the computer keyboard to pause playing, press `enter` to continue playing. After current playing is finished, by default you can press `ctrl` to play again. All of these key settings can be customized in the config file, please look at the settings manual.



## Is there a compatible version for Linux and macOS?

There are Linux and macOS compatible versions, you can download at the [release page](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest) of Ideal Piano on github. For the installation of Linux and macOS versions, here are the instructions.

### Linux

You can download the Linux compatible version from the release page, which contains the Linux executable for Ideal Piano, double click to open the software to use.

You can download this software for Windows, Linux and macOS from the [release page](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest).

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



## What should I pay attention to when playing with a MIDI keyboard?

It is better to open Ideal Piano only after the midi keyboard is connected to the computer, or open Ideal Piano first, don't click the midi keyboard button, then connect the midi keyboard to the computer, then click the button, so as to make sure your midi keyboard can be detected properly in the software. If the midi keyboard still does not respond, then press `shift` on your computer keyboard to display the MIDI ports currently available on your computer, you can confirm the MIDI port number you need to use by the name of the corresponding device, then open `change_settings.exe` to change the value of `midi_device_id` to the one you want to use MIDI port number, then reopen Ideal Piano.



## Why can't Ideal Piano detect my MIDI keyboard?

If you open the DAW, the midi keyboard is already available in the DAW, then Ideal Piano can't detect your midi keyboard at this time, because a midi keyboard can only control one software at most, so at this time the DAW has already occupied the midi keyboard, and Ideal Piano can't detect the midi keyboard.

If you want to use a midi keyboard in a DAW and also use Ideal Piano, there is a very simple solution.
Using `loopmidi`, a free software, you can use both DAW and Ideal Piano to play midi keyboard, the procedure is as follows.



## How to use Ideal Piano with DAW?

### Using a MIDI keyboard in the DAW

With `loopmidi`, a free software, you can play with a midi keyboard in the DAW, and at the same time Ideal Piano can display the current notes and the corresponding chords, so you can listen to the instrument you want more easily and see what you are playing in Ideal Piano.

Take FL Studio for example, first open loopmidi, create a new midi port, (click on the + sign below) and then open FL Studio, in the midi settings in the options, select the midi keyboard you are connected to on the input side, and select the new midi port you just created on the output side.

The input midi keyboard should be enabled, the port should not be set (left blank), and the output midi port should be set with a port number, for example 0.

Then load an instrument sound source and set the midi output port number for this instrument to the same number as the output midi port.

Then open Ideal Piano, change the midi_device_id in the config.py file to the number of the new midi port in loopmidi, and remember to set the parameter load_sound to False, so that Ideal Piano will not load the sound source you set, and will only play the sound source in the host when you play it. so that Ideal Piano will not load the sources it has set up, and will only play the sources from the host when playing.

For some sources, even if the midi output port is set to the same loopmidi as the host, the solution is to use the midi out plugin, set the port to the same midi output port as the host, then set the input port of the source to the midi out port, and select the midi out channel to play when you play to receive the data. (Another important point is that

(There is also a very important point is that you must first import the source, and then import the midi out plug-in, and then set the port, every time you change the new source to this order, otherwise the data still can not pass loopmidi)

### Play the project in the DAW

With loopmidi you can also play the project in the DAW and at the same time Ideal Piano can demonstrate the current notes and chords, you just need to set the midi out port of the DAW and the midi out port of the source to the same number, which corresponds to the new midi port you created in loopmidi.

For example, if loopmidi creates a new midi port called midi port A, then in the midi settings of the DAW, set the port corresponding to midi port A to 0, then set the midi output port of the audio source to 0 as well, and then set the midi_device_id in the configuration file of Ideal Piano to the number corresponding to midi port A.

Save the settings file after each change (or just open change_settings.exe to search for parameters to modify more easily), then reopen Ideal Piano.exe. Then click the midi keyboard button to enter midi keyboard mode, at this time, play the track with the midi output port set in the DAW. When you play the track with the midi output port, you can see that Ideal Piano also follows the same notes in real time.

For some sources that are set up with midi out but still can't pass data to loopmidi, the solution is also to use midi out as a relay station, but this is slightly different from playing with a midi keyboard.

When playing with a midi keyboard, you can select the midi out track to play, and the sound will come from the source paired with the midi port, and Ideal Piano can also receive the midi signal, but if you don't use the midi keyboard and play the project directly in the DAW, you can't transfer the data to loopmidi even if you select the midi out track to play. I found a solution to this problem by copying the pairing and playing the track.

The solution I found was to copy the notes from the track of the source paired with the midi port to the piano window of midi out, then mute the track of that source and let midi out play only, then I could hear the sound of the track of the source when it was not muted before, and I could also transfer data to loopmidi, so Ideal Piano could also can receive the midi signal in real time.



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

