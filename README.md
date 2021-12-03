# Ideal-Piano

English [中文](#Ideal-Piano-1)

## Introduction

This is a smart piano software that I started to develop in April 2020 and recently near completion in early August. This smart piano software has some usefulness for music beginners, musicians, music lovers, etc. 

The best feature of Ideal Piano is the algorithm that uses music logic to determine what chord the currently played note is composed of and display it on the screen. This algorithm is a project of my own, a music logic algorithm designed by musicpy, a music composition language library, and it works very well, including all root position chords, all kinds of chord inversions, voicings and chords which have altered notes, omissions, etc. It can determine very complicated chord compositions, and there are several parameters to adjust the priority of the music logic. (The default parameter settings are the most widely applicable)

## Usage

There are three modes in total: computer keyboard free play, MIDI keyboard free play and play MIDI file to analyze chords and demonstrate them in real time. In the demo mode of playing the MIDI file, you can choose to remove the main melody by the algorithm and listen only to the notes of the chords in the bass part. These three modes can be accessed by selecting the corresponding buttons in the upper left corner after opening Ideal Piano.

The first mode, computer keyboard free play, the default keys are in the file `config.py`, if you want to change the notes corresponding to the keyboard, you can change them directly in `config.py` and save them. This mode is mainly provided to someone who do not have any MIDI keyboard to play in spare time.

The second mode, MIDI keyboard free play, is to connect a MIDI keyboard to your computer and then enter this mode, you can play on the MIDI keyboard, and the software will show you the position of the current note in the corresponding piano, and at the same time analyze in real time what chords you are currently playing (the root note plus the full expression of the chord type), and display them on the screen. You can set the path and the file type of the sound source (wav, mp3, ogg, etc.) in `config.py`.

Previously I wanted to implement a MIDI keyboard shared by both DAW (arranger host) and Ideal Piano, or to play a project in DAW and display the current notes in Ideal Piano, but at the beginning it failed, always showing errors like Host error, but later I found a good solution. loopMIDI is a free software that allows you to create virtual MIDI ports, so you can use it to connect to the MIDI ports of several different software. With loopMIDI you can use a MIDI keyboard for both the DAW and Ideal Piano, so you can load the source you want to hear in the DAW and then play it on the MIDI keyboard and hear the DAW source, while Ideal Piano can display the chord type and notes you are currently playing in real time.

In addition, it is also possible to play a project in the DAW and have Ideal Piano display the chord types and notes being played at the same time. The procedure is described in `User Manuals/English/User Instructions (Read me first!).pdf`, please check it out.

The third mode is to play the MIDI file to analyze the current chords in real time. After entering this mode, a file browsing box will pop up for you to select the MIDI file you want to play in Ideal Piano, and after that, you can select the MIDI track you want to play and the range you want to play (according to the percentage, for example, you can enter 0 and 50 in the range to play the first half), you can also choose the BPM (tempo of the song) to be played.

You can also choose to remove the main melody through the algorithm and listen only to the notes of the chords in the bass part. (The algorithm to remove the main melody of the tune is my own idea, and after testing, it works well for most of the pieces.)

A special note here is that the MIDI track box can be left blank, and the program I wrote will intelligently find the first track with notes in the MIDI file you choose and use it as the track to play. So if it is a pure piano piece with only one track, then you can leave it blank and the program will play the track with the notes directly, if it is a MIDI with multiple tracks, then you can fill in the track you want to play according to your needs.

In this mode, the selected MIDI file will be played in Ideal Piano, with the sound coming from a built-in General MIDI player by default. You can change `play_as_midi` in the settings file to `False` to make the sound coming from the sound source you set. The sound source must be a folder with audio files named after notes, like `C5.wav`. The current position of the notes on the piano will be displayed on the screen, and the chords of the notes currently played will be analyzed in real time.

If you want the sound to come from a sound source in a DAW, you can use loopMIDI. Playing the project in the DAW, while Ideal Piano receives the MIDI signal and analyzes the chords in real time, displaying the notes and chord types on the screen. For more details, please go to the file `User Manuals/English/User Instructions (Read me first!).pdf`.

This software also supports directly loading SoundFont files as sound source to play by keyboard and play MIDI files, please refer to changelog in `User Manuals` folder to see how to use it.

## Download

You can download this software for Windows and Linux from the [release page](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest), currently Ideal Piano is not compatible with macOS because many dependent python packages of this software has serious existing bugs with macOS when testing, I will try to make a compatible version for it in my spare time.

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

1. It seems that some people fails to download directly from github, so I also upload a copy to the cloud, you can download directly from [here](https://www.jianguoyun.com/p/DZN6-TAQhPG0CBifnp0E)
2. Since my software is in English, I made a Chinese patch package, which includes: the buttons of the interface, the names of the chord types displayed, the single note and intervals, the interface for selecting MIDI files and each setting item, the programs for changing the settings. The download link of the Chinese patch installation package is [here](https://www.jianguoyun.com/p/DabhR74QhPG0CBi3vrID)
3. The various setting parameters of this software can be modified using `tools/change_settings.exe` or directly in `config.py`, save and then open the software to see the changes.

## Summary

Since this project is entirely done by myself, my artwork is not good, so Ideal Piano can be used very smoothly if you are not very picky about the artwork.

If you encounter any problems when using this software, please take a look at the user manual first, if you cannot solve the problem, you can contact me by sending emails to 2180502841@qq.com or adding my qq number 2180502841, thank you for your support~

The chord logic algorithm used in this software comes from another project of mine, a chord judgment algorithm I designed in musicpy, a professional music theory composition language, which follows the logic of music theory completely. The algorithm to remove the main melody is also from my project musicpy, so you can say that this smart piano software is one of the practical applications of musicpy. If you are interested in the musicpy project, please check my repository, the link is [here](https://github.com/Rainbow-Dreamer/musicpy)

# Ideal-Piano

[English](#Ideal-Piano) 中文

## 介绍

这是一款智能钢琴软件，我在2020年的4月份开始开发，最近8月初接近完工。这款智能钢琴软件对于音乐初学者，音乐人，音乐爱好者等都有一些用处。

Ideal Piano最大的特色就是通过乐理逻辑的算法来判断当前演奏的音组成的是什么和弦，并且显示在屏幕上。这个算法是自己的一个项目， 乐理作曲语言库musicpy里面自己精心设计的一个乐理逻辑算法，判断的效果非常好，包括所有的原位和弦，各种和弦的转位，voicings 和变化音，省略音等等，可以判断非常覆杂的和弦组成，并且有多个乐理逻辑判断优先级的参数可以调整。 （默认的参数设置的适用性最广泛）

## 使用

这个智能钢琴软件总共有三个模式，电脑键盘自由演奏，MIDI键盘自由演奏和播放MIDI文件分析和弦并且实时演示。在播放MIDI文件演示的模式中，可以选择通过算法去除主旋律，只听低音部分的和弦的音符。这三个模式在打开Ideal Piano之后选择左上角对应的按钮就可以进入。

第一个模式，电脑键盘自由演奏，默认的键位在`config.py`这个文件里，如果想要改变键盘对应的音符，直接在`config.py`里改然后保存即可。这个模式主要提供给没有任何MIDI键盘的小伙伴平时可以弹着玩。

第二个模式，MIDI键盘自由演奏，接上MIDI键盘到电脑，然后进入这个模式，就可以在MIDI键盘上演奏，并且软件里同时会显示你当前弹的音在对应的钢琴的位置， 同时实时分析你当前弹下的音组成的是什么和弦（根音加上和弦类型的完整表述），并且显示在屏幕上。音源可以自己在`config.py`里设置路径和音源的文件类型 （wav, mp3, ogg等等）。

之前我想实现同时DAW（编曲宿主）和Ideal Piano共用一个MIDI键盘，或者DAW里面播放工程同时Ideal Piano也可以显示当前的音符， 可是在一开始遭遇了失败，一直都是显示Host error之类的错误，后来我找到了很好的解决办法。 loopMIDI这个免费软件可以做到建立虚拟MIDI端口， 因此可以用来连接多个不同的软件的MIDI端口。使用loopMIDI可以让DAW和Ideal Piano同时使用一个MIDI键盘，这样你就可以在DAW里面加载自己想听的音源， 然后在MIDI键盘上演奏，听到的是DAW的音源，与此同时Ideal Piano也可以同步地实时显示当前演奏的和弦类型和音符。

除此之外，也可以实现在DAW里播放工程， 同时Ideal Piano也可以显示当下演奏的和弦类型和音符。具体的操作流程我在`User Manuals/中文/使用须知 (请先看我!).pdf`里面写的很详细，请大家去看看。

第三个模式，播放MIDI文件实时分析当前的和弦，进入这个模式后，会弹出一个文件浏览框让大家选择想要在Ideal Piano里播放的MIDI文件，选择完成之后， 可以选择自己想要播放的MIDI轨道，选择播放的范围（按照百分比来算，比如播放前半段就可以在范围那边写0和50），也可以选择播放的BPM（曲速）。

也可以选择通过算法去除主旋律，只听低音部分的和弦的音符。(这个去除曲子的主旋律的算法是我自己想的，经过实测，对于大部分曲子的效果还是不错的)

这里需要特别说明的是，MIDI轨道那个框可以留空不用填，我写的程序会智能查找你选择的MIDI文件里的第一个有音符的轨道并且作为播放的轨道。因此如果是那种只有一个轨道的纯钢琴曲，那么就可以留空不用填，程序会直接播放那个有音符的轨道，如果是有多个轨道的MIDI，那么就根据自己的需要填入想要播放的轨道即可。

在这个模式下，选择的MIDI文件会在Ideal Piano里播放，声音默认来自一个内置的General MIDI播放器。你可以把配置文件里的`play_as_midi`改为`False`让声音来自于自己设置好的音源。音源必须是一个文件夹里面是以音符为名字的音频文件，比如`C5.wav`这种。在画面上会显示当前的音符在钢琴上的位置，并且实时分析当前演奏的音符组成的和弦。

如果你想要声音来自DAW的音源的话，使用loopMIDI就可以做到了，在DAW里播放工程，同时Ideal Piano可以同步接收到MIDI信号，实时分析当前的音符组成的和弦，显示音符与和弦类型在屏幕上。具体的操作流程请到`User Manuals/中文/使用须知 (请先看我!).pdf`这个文件里看。

本软件也支持直接加载SoundFont文件作为音源来用键盘演奏和播放MIDI文件，请参考`User Manuals`文件夹中的更新日志以了解如何使用。

## 下载

你可以从[release页面](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest)下载这个软件的Windows和Linux版本，目前Ideal Piano不兼容macOS，因为这个软件的许多依赖的python包在测试时与macOS之间存在严重的bug，我将在业余时间尝试为它制作一个兼容版本。

## 预览

以下是Ideal Piano的画面预览：

![image](previews/1.jpg)

<p align="center">打开Ideal Piano的初始页面</p>

![image](previews/2.jpg)

<p align="center">演奏时显示音符并且实时通过乐理逻辑分析判断当前演奏的音组成的和弦类型</p>

![image](previews/3.jpg)

<p align="center">选择MIDI文件播放的窗口</p>

![image](previews/4.jpg)

<p align="center">音符条下落模式</p>

![image](previews/5.jpg)

<p align="center">你可以轻松地改变背景图片</p>

## 其他说明

1. 好像有些人github下载失败，所以我坚果云也传了一份，直接可以从[这里](https://www.jianguoyun.com/p/DZN6-TAQhPG0CBifnp0E)下载
2. 由于我这个软件是全英文的，考虑到很多小伙伴可能看中文的和弦类型名称比较亲切一些，因此我做了一个中文补丁包，变成中文的内容包括：界面的按钮，显示的和弦种类名称，单音和音程，选择MIDI文件的界面和每个设置项，更改设置的程序。中文补丁安装包的下载地址在[这里](https://www.jianguoyun.com/p/DabhR74QhPG0CBi3vrID)
3. 这个软件的各种参数设置都可以使用`tools/change_settings.exe`修改或者直接到`config.py`里去修改，保存之后再打开软件就可以看到变化了。

## 总结

由于这个项目完全由本人一个人完成，本人的美工水平欠佳，因此只要不是对于美工很挑剔的话，Ideal Piano还是可以用的很顺畅的。

如果你在使用这个软件时有遇到任何问题，请先看使用手册，如果你无法解决问题，请发邮件到2180502841@qq.com或者加我的qq号2180502841，感谢大家的支持~

这个软件在实时和弦判断用到的乐理逻辑算法来自于我的另一个项目，专业乐理作曲语言musicpy里我精心设计的一个和弦判断的算法，完全按照乐理的逻辑来推测。在播放MIDI的模式下可以选择去除主旋律，这个去除主旋律的算法也同样来自我的项目musicpy，所以可以说这个智能钢琴软件就是musicpy的其中一个实际应用。对musicpy这个项目感兴趣的欢迎来看我的repository，链接在[这里](https://github.com/Rainbow-Dreamer/musicpy)
