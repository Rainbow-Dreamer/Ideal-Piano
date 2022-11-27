# Ideal-Piano

[中文](https://github.com/Rainbow-Dreamer/Ideal-Piano/blob/master/README_cn.md)

## Introduction

This is a smart piano software that I started to develop in April 2020.

The best feature of Ideal Piano is that it uses algorithm based on music theory to determine what chord types you are currently playing and displays it on the screen. This algorithm comes from my another project [musicpy](https://github.com/Rainbow-Dreamer/musicpy), a python library to compose and analyze music, if you are interested in it, please check it. This algorithm could detect all root position chords, chord inversions, voicings and chords which have altered notes, omissions, from simple chords to very complex chords.



## Functionality

* You can use your computer keyboard or MIDI keyboard to play, keyboard mappings with notes could be customized in the settings file
* Analyze what chord types you are playing in details and display on the screen
* Choose MIDI files to playback in waterfall form, show current chord types in real time
* You can choose to split the melody and chord parts of MIDI files and play only one of them, using music analysis algorithm based on music theory
* You can choose to analyze current key you are playing or MIDI files in real time using music analysis algorithm based on music theory, supporting major, minor and church modes like dorian, lydian (experimental)
* Load audio files or SoundFont files as instruments
* Connect with DAW and analyze chord types that is currently playing in the DAW
* Fully customizable UI, easily change background image, font type, font size, customize piano keyboard, etc.
* You can choose to display corresponding note names on piano keys (by default the note names are not displayed on the piano keys)



## Cross-platform

Ideal Piano currently supports Windows, Linux and macOS. Please see the download section of README.



## Usage

Please check user instructions in `User Manuals` folder, which provides detailed instructions of how to use each functionality of Ideal Piano. The settings manual in the  same folder is also worth checking, as it describes what each setting parameter in the settings file is, so you can customize Ideal Piano through modifying setting parameters.




## Download

You can download this software for Windows, Linux and macOS from the [release page](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest).

Note1: for Linux version, playing MIDI files using default settings requires installing freepats and timidity. On Ubuntu you can run

```
sudo apt-get install freepats timidity
```

If you want to use SoundFont files as instruments in the Linux version, you need to install fluidsynth, you can refer to [here](https://github.com/FluidSynth/fluidsynth/wiki/Download) for the install command for different Linux distributions. For Ubuntu, it is

```
sudo apt-get install fluidsynth
```

Note2: for macOS version, due to an existing bug of pygame's mixer that it cannot pause MIDI file playing on macOS, before the pygame's developers fix this bug, the default settings of playing MIDI files cannot pause for the macOS version. If you want to pause and unpause MIDI files when playing for macOS version, you can switch to use fluidsynth to play MIDI files in Ideal Piano by changing `use_soundfont` to True in the settings file, and then install fluidsynth on macOS, it is pretty easy, you can use homebrew to install fluidsynth by running this line in the terminal

```
brew install fluidsynth
```



## Previews

Here is a preview of Ideal Piano:

![image](previews/1.jpg)

<p align="center">the initial screen of Ideal Piano</p

![image](previews/2.jpg)

<p align="center">Display notes you are current playing, analyze the chord types and display on the screen</p

![image](previews/3.jpg)

<p align="center">Window for selecting MIDI files to play</p

![image](previews/4.jpg)

<p align="center">Note bar drop mode</p

![image](previews/5.jpg)

<p align="center">You can simply drag an image file to the screen to change the background</p>



## Other notes

Currently supported languages only include English and Chinese, you can change the language by change the setting parameter `language`.



## Summary

If you encounter any problems when using this software, please take a look at the user manual first, if you cannot solve the problem, you can contact me by sending emails to 2180502841@qq.com, thank you for your support~

