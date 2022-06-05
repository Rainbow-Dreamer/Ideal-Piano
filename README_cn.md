# Ideal-Piano

## 介绍

这是一款智能钢琴软件，我在2020年的4月份开始开发，最近8月初接近完工。这款智能钢琴软件对于音乐初学者，音乐人，音乐爱好者等都有一些用处。

Ideal Piano最大的特色就是通过乐理逻辑的算法来判断当前演奏的音组成的是什么和弦，并且显示在屏幕上。这个算法是自己的一个项目， 乐理作曲语言库musicpy里面自己精心设计的一个乐理逻辑算法，判断的效果非常好，包括所有的原位和弦，各种和弦的转位，voicings 和变化音，省略音等等，可以判断非常复杂的和弦组成，并且有多个乐理逻辑判断优先级的参数可以调整。（默认的参数设置的适用性最广泛）

这个钢琴软件现在有Windows, Linux 和 macOS版本。



## 使用

这个智能钢琴软件总共有三个模式，电脑键盘自由演奏，MIDI键盘自由演奏和播放MIDI文件分析和弦并且实时演示。这三个模式在打开Ideal Piano之后选择左上角对应的按钮就可以进入。

第一个模式，电脑键盘自由演奏，默认的键位在`piano_config.py`这个文件里，如果想要改变键盘对应的音符，直接在`piano_config.py`里改然后保存即可。这个模式主要提供给没有任何MIDI键盘的小伙伴平时可以弹着玩。

第二个模式，MIDI键盘自由演奏，接上MIDI键盘到电脑，然后进入这个模式，就可以在MIDI键盘上演奏，并且软件里同时会显示你当前弹的音在对应的钢琴的位置， 同时实时分析你当前弹下的音组成的是什么和弦（根音加上和弦类型的完整表述），并且显示在屏幕上。音源可以自己在`piano_config.py`里设置路径和音源的文件类型 （wav, mp3, ogg等等）。除此之外，也可以实现同时DAW和Ideal Piano共用一个MIDI键盘，或者在DAW里播放工程， 同时Ideal Piano也可以显示当下演奏的和弦类型和音符。具体的操作流程我在`User Manuals/中文/使用须知 (请先看我!).pdf`里面写的很详细，请大家去看看。

第三个模式，播放MIDI文件实时分析当前的和弦，进入这个模式后，会弹出一个文件浏览框让大家选择想要在Ideal Piano里播放的MIDI文件，选择完成之后， 可以选择自己想要播放的MIDI轨道，也可以选择播放的BPM（曲速），也可以选择通过算法去除主旋律，只听低音部分的和弦的音符。(这个去除曲子的主旋律的算法是我自己想的，经过实测，对于大部分曲子的效果还是不错的)

这个软件的各种参数设置都可以点击主屏幕上的`Settings`修改，之后再打开软件就可以看到变化了，也可以点击主屏幕上的设置按钮打开设置。

本软件也支持直接加载SoundFont文件作为音源来用键盘演奏和播放MIDI文件，请参考`User Manuals`文件夹中的更新日志以了解如何使用。

你可以设置 `show_chord_details` 为 `True` 来显示你当前正在演奏的和弦的详细信息，这对于学习和理解和弦结构有帮助。



## 下载

你可以从[release页面](https://github.com/Rainbow-Dreamer/Ideal-Piano/releases/latest)下载这个软件的Windows, Linux和macOS版本。

注意1：对于Linux版本，使用默认设置播放MIDI文件需要安装freepats 和 timidity。在Ubuntu上，你可以运行

````
sudo apt-get install freepats timidity
````

如果你想在Linux版本中使用SoundFont文件作为乐器，你需要安装fluidsynth，你可以参考[这里](https://github.com/FluidSynth/fluidsynth/wiki/Download)了解不同Linux发行版的安装命令。对于Ubuntu，它是

````
sudo apt-get install fluidsynth
````

注意2：对于macOS版本，由于pygame的mixer存在一个bug，即在macOS上不能暂停播放MIDI文件，在pygame的开发者修复这个bug之前，macOS版本播放MIDI文件的默认设置不能暂停。如果你想在macOS版本上播放MIDI文件时暂停和取消暂停，你可以在Ideal Piano的设置文件中把`use_soundfont`改为True，改用fluidsynth来播放MIDI文件，然后在macOS上安装fluidsynth，这很简单，你可以用homebrew在terminal运行这一行来安装fluidsynth

``````
brew install fluidsynth
``````



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

1. 好像有些人github下载失败，所以我坚果云也传了一份，直接可以从[这里](https://www.jianguoyun.com/p/DY_8cucQhPG0CBifkqYE)下载
2. 由于我这个软件是全英文的，考虑到很多小伙伴可能看中文的和弦类型名称比较亲切一些，因此我做了一个中文补丁包，请将设置文件里的`language`改为`'Chinese'`，保存后重启软件即可使用。



## 总结

由于这个项目完全由本人一个人完成，本人的美工水平欠佳，因此只要不是对于美工很挑剔的话，Ideal Piano还是可以用的很顺畅的。

如果你在使用这个软件时有遇到任何问题，请先看使用手册，如果你无法解决问题，请发邮件到2180502841@qq.com或者加我的qq号2180502841，感谢大家的支持~

这个软件在实时和弦判断用到的乐理逻辑算法来自于我的另一个项目，专业乐理作曲语言musicpy里我精心设计的一个和弦判断的算法，完全按照乐理的逻辑来推测。在播放MIDI的模式下可以选择去除主旋律，这个去除主旋律的算法也同样来自我的项目musicpy，所以可以说这个智能钢琴软件就是musicpy的其中一个实际应用。对musicpy这个项目感兴趣的欢迎来看我的repository，链接在[这里](https://github.com/Rainbow-Dreamer/musicpy)

