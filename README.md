# Ideal-Piano

[中文](https://github.com/Rainbow-Dreamer/Ideal-Piano/blob/master/README_cn.md)

## Introduction

This is a smart piano software that I started to develop in April 2020 and recently near completion in early August. This smart piano software has some usefulness for music beginners, musicians, music lovers, etc.

The best feature of Ideal Piano is the algorithm that uses music logic to determine what chord the currently played note is composed of and display it on the screen. This algorithm is a project of my own, a music logic algorithm designed by musicpy, a music composition language library, and it works very well, including all root position chords, all kinds of chord inversions, voicings and chords which have altered notes, omissions, etc. It can determine very complicated chord compositions, and there are several parameters to adjust the priority of the music logic. (The default parameter settings are the most widely applicable)

This piano software currently has Windows, Linux and macOS version.

## Usage

There are three modes in total: computer keyboard free play, MIDI keyboard free play and play MIDI file to analyze chords and demonstrate them in real time. In the demo mode of playing the MIDI file, you can choose to remove the main melody by the algorithm and listen only to the notes of the chords in the bass part. These three modes can be accessed by selecting the corresponding buttons in the upper left corner after opening Ideal Piano.

The first mode, computer keyboard free play, the default keys are in the file `piano_config.py`, if you want to change the notes corresponding to the keyboard, you can change them directly in `piano_config.py` and save them. This mode is mainly provided to someone who do not have any MIDI keyboard to play in spare time.

The second mode, MIDI keyboard free play, is to connect a MIDI keyboard to your computer and then enter this mode, you can play on the MIDI keyboard, and the software will show you the position of the current note in the corresponding piano, and at the same time analyze in real time what chords you are currently playing (the root note plus the full expression of the chord type), and display them on the screen. You can set the path and the file type of the sound source (wav, mp3, ogg, etc.) in `piano_config.py`.

Previously I wanted to implement a MIDI keyboard shared by both DAW (arranger host) and Ideal Piano, or to play a project in DAW and display the current notes in Ideal Piano, but at the beginning it failed, always showing errors like Host error, but later I found a good solution. loopMIDI is a free software that allows you to create virtual MIDI ports, so you can use it to connect to the MIDI ports of several different software. With loopMIDI you can use a MIDI keyboard for both the DAW and Ideal Piano, so you can load the source you want to hear in the DAW and then play it on the MIDI keyboard and hear the DAW source, while Ideal Piano can display the chord type and notes you are currently playing in real time.

In addition, it is also possible to play a project in the DAW and have Ideal Piano display the chord types and notes being played at the same time. The procedure is described in `User Manuals/English/User Instructions (Read me first!).pdf`, please check it out.

The third mode is to play the MIDI file to analyze the current chords in real time. After entering this mode, a file browsing box will pop up for you to select the MIDI file you want to play in Ideal Piano, and after that, you can select the MIDI track you want to play and the range you want to play (according to the percentage, for example, you can enter 0 and 50 in the range to play the first half), you can also choose the BPM (tempo of the song) to be played.

You can also choose to remove the main melody through the algorithm and listen only to the notes of the chords in the bass part. (The algorithm to remove the main melody of the tune is my own idea, and after testing, it works well for most of the pieces.)

A special note here is that the MIDI track box can be left blank, and the program I wrote will intelligently find the first track with notes in the MIDI file you choose and use it as the track to play. So if it is a pure piano piece with only one track, then you can leave it blank and the program will play the track with the notes directly, if it is a MIDI with multiple tracks, then you can fill in the track you want to play according to your needs.

In this mode, the selected MIDI file will be played in Ideal Piano, with the sound coming from a built-in General MIDI player by default. You can change `play_as_midi` in the settings file to `False` to make the sound coming from the sound source you set. The sound source must be a folder with audio files named after notes, like `C5.wav`. The current position of the notes on the piano will be displayed on the screen, and the chords of the notes currently played will be analyzed in real time.

If you want the sound to come from a sound source in a DAW, you can use loopMIDI. Playing the project in the DAW, while Ideal Piano receives the MIDI signal and analyzes the chords in real time, displaying the notes and chord types on the screen. For more details, please go to the file `User Manuals/English/User Instructions (Read me first!).pdf`.

This software also supports directly loading SoundFont files as sound source to play by keyboard and play MIDI files, please refer to changelog in `User Manuals` folder to see how to use it.

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

 It is also recommended to install fluidsynth by MacPorts, which might be faster than homebrew, and also very easy to install, you can click this [link](https://ports.macports.org/port/fluidsynth/) to install MacPorts and then install fluidsynth using MacPorts with the command provided by the website.

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

1. It seems that some people fails to download directly from github, so I also upload a copy to the cloud, you can download directly from [here](https://www.jianguoyun.com/p/DY_8cucQhPG0CBifkqYE)
2. Since my software is in English, considering somebody might be more familiar with chord type names in Chinese, I made a Chinese patch package, please change `language` to `'Chinese'` in the settings file, save and restart the software to use it.
3. The various setting parameters of this software can be modified using `tools/change_settings.exe` or directly in `piano_config.py`, save and then open the software to see the changes.

## Summary

Since this project is entirely done by myself, my artwork is not good, so Ideal Piano can be used very smoothly if you are not very picky about the artwork.

If you encounter any problems when using this software, please take a look at the user manual first, if you cannot solve the problem, you can contact me by sending emails to 2180502841@qq.com or adding my qq number 2180502841, thank you for your support~

The chord logic algorithm used in this software comes from another project of mine, a chord judgment algorithm I designed in musicpy, a professional music theory composition language, which follows the logic of music theory completely. The algorithm to remove the main melody is also from my project musicpy, so you can say that this smart piano software is one of the practical applications of musicpy. If you are interested in the musicpy project, please check my repository, the link is [here](https://github.com/Rainbow-Dreamer/musicpy)
