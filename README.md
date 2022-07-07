# Ideal-Piano

[中文](https://github.com/Rainbow-Dreamer/Ideal-Piano/blob/master/README_cn.md)

## Introduction

This is a smart piano software that I started to develop in April 2020 and recently near completion in early August. This smart piano software has some usefulness for music beginners, musicians, music lovers, etc.

The best feature of Ideal Piano is the algorithm that uses music logic to determine what chord the currently played note is composed of and display it on the screen. This algorithm is a project of my own, a music logic algorithm designed by musicpy, a music composition language library, and it works very well, including all root position chords, all kinds of chord inversions, voicings and chords which have altered notes, omissions, etc. It can determine very complicated chord compositions, and there are several parameters to adjust the priority of the music logic. (The default parameter settings are the most widely applicable)

This piano software currently has Windows, Linux and macOS version.



## Usage

There are three modes in total: computer keyboard free play, MIDI keyboard free play and play MIDI file to analyze chords and demonstrate them in real time. You can enter these three modes by selecting the corresponding buttons in the upper left corner after opening Ideal Piano.

The first mode, computer keyboard free play, the default keys are in the file `piano_config.py`, if you want to change the notes corresponding to the keyboard, you can change them directly in `piano_config.py` and save them. This mode is mainly provided to someone who do not have any MIDI keyboard to play in spare time.

The second mode, MIDI keyboard free play, is to connect a MIDI keyboard to your computer and then enter this mode, you can play on the MIDI keyboard, and the software will show you the position of the current note in the corresponding piano, and at the same time analyze in real time what chords you are currently playing (the root note plus the full expression of the chord type), and display them on the screen. You can set the path and the file type of the sound source (wav, mp3, ogg, etc.) in `piano_config.py`. In addition, it is also possible to use a MIDI keyboard with both DAW and Ideal Piano, or to play a project in the DAW and have Ideal Piano display the chord types and notes being played at the same time. The steps is described in `User Manuals/English/User Instructions (Read me first!).pdf`, please check it out.

The third mode is to play the MIDI file to analyze the current chords in real time. After entering this mode, a file browsing box will pop up for you to select the MIDI file you want to play in Ideal Piano, and after that, you can select the MIDI track you want to play, choose the BPM (tempo of the song) to be played, and you can also choose to remove the main melody through the algorithm and listen only to the notes of the chords in the bass part. (The algorithm to remove the main melody of the tune is my own idea, and after testing, it works well for most of the pieces.)

The various setting parameters of this software can be modified by clicking `SETTINGS` button on the main screen to open the change settings window, save and then close the change settings window, the changes will take place immediately.

This software also supports directly loading SoundFont files as sound source to play by keyboard and play MIDI files, please refer to changelog in `User Manuals` folder to see how to use it.

You can set `show_chord_details` to `True` to show chord details of current chord you are playing, which is helpful for learning and understanding chord structures.

You can set `show_note_name_on_piano_key` to `True` to show note names on piano keys, by default, only the starting C notes will be shown, if you want to show all note names, you can set `show_only_start_note_name` to `False`, which will show all note names on white keys.



## Download

You can download this software for Windows, Linux and macOS from the [release page](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest).

Note1: for Linux version,  playing MIDI files using default settings requires installing freepats and timidity. On Ubuntu you can run

````
sudo apt-get install freepats timidity
````

If you want to use SoundFont files as instruments in the Linux version, you need to install fluidsynth, you can refer to [here](https://github.com/FluidSynth/fluidsynth/wiki/Download) for the install command for different Linux distributions. For Ubuntu, it is

````
sudo apt-get install fluidsynth
````

Note2: for macOS version, due to an existing bug of pygame's mixer that it cannot pause MIDI file playing on macOS, before the pygame's developers fix this bug, the default settings of playing MIDI files cannot pause for the macOS version. If you want to pause and unpause MIDI files when playing for macOS version, you can switch to use fluidsynth to play MIDI files in Ideal Piano by changing `use_soundfont` to True in the settings file, and then install fluidsynth on macOS, it is pretty easy, you can use homebrew to install fluidsynth by running this line in the terminal

``````
brew install fluidsynth
``````



## Previews

Here is a preview of Ideal Piano's screen.

![image](previews/1.jpg)

<p align="center">Opening the initial page of Ideal Piano</p

![image](previews/2.jpg)

<p align="center">Displays notes as they are played and determines the chord type of the currently played note in real time by logical analysis of the music theory</p

![image](previews/3.jpg)

<p align="center">Window for selecting MIDI files to play</p

![image](previews/4.jpg)

<p align="center">Note bar drop mode</p

![image](previews/5.jpg)

<p align="center">You can easily change the background image</p>



## Other notes

1. Since my software is in English, considering somebody might be more familiar with chord type names in Chinese, I made a Chinese patch package, please change `language` to `'Chinese'` in the settings file, save and restart the software to use it.



## Summary

Since this project is entirely done by myself, my artwork is not good, so Ideal Piano can be used very smoothly if you are not very picky about the artwork.

If you encounter any problems when using this software, please take a look at the user manual first, if you cannot solve the problem, you can contact me by sending emails to 2180502841@qq.com or adding my qq number 2180502841, thank you for your support~

The chord logic algorithm used in this software comes from another project of mine, a chord judgment algorithm I designed in musicpy, a professional music theory composition language, which follows the logic of music theory completely. The algorithm to remove the main melody is also from my project musicpy, so you can say that this smart piano software is one of the practical applications of musicpy. If you are interested in the musicpy project, please check my repository, the link is [here](https://github.com/Rainbow-Dreamer/musicpy)
