# Ideal-Piano

## 介绍

这是一款智能钢琴软件，是我在2020年4月开始开发的。

Ideal Piano的最大特点是，它使用基于乐理的算法来确定你目前正在弹奏的和弦类型，并将其显示在屏幕上。这个算法来自我的另一个项目[musicpy](https://github.com/Rainbow-Dreamer/musicpy)，一个可以用来作曲和分析音乐的python库，如果你对它感兴趣，欢迎查看一下。这个算法可以检测出所有的原位和弦，和弦转位，和弦声部排列，有变化音和省略音的和弦，从简单的和弦到非常复杂的和弦。



## 功能

* 你可以使用你的电脑键盘或MIDI键盘来演奏，键盘与音符的映射可以在设置文件中自定义
* 详细分析你正在演奏的和弦类型，并显示在屏幕上
* 选择MIDI文件使用瀑布流形式播放，实时显示当前的和弦类型，也可以选择显示当前和弦的详细乐理信息
* 支持播放多轨的MIDI文件，播放时点击进度条即可改变播放进度
* 你可以选择分离MIDI文件的旋律和和弦部分，只播放其中一个，使用基于乐理的音乐分析算法
* 你可以选择使用基于乐理的音乐分析算法，实时分析你正在演奏或MIDI文件的当前调式，支持大调、小调和中古调式，比如dorian, lydian（实验性功能）
* 加载音频文件或SoundFont文件作为乐器
* 与DAW连接，分析当前在DAW中播放的和弦类型
* 完全可定制的用户界面，轻松改变背景图片、字体类型、字体大小、定制钢琴键盘等
* 你可以选择在钢琴键上显示对应的音符名称（默认情况下，音符名称不显示在钢琴键上）



## 跨平台

Ideal Piano目前支持Windows, Linux和macOS。请看README的下载部分。

Windows: 在Windows 7, 10, 11上测试通过

Linux：在Ubuntu 21.10上测试通过

macOS：在macOS 12上测试通过



## 使用

请查看`User Manual`文件夹中的使用须知，其中详细说明了如何使用Ideal Piano的各项功能。同一文件夹中的设置参数说明书也可以看一下，它介绍了设置文件中的每个设置参数是什么，因此你可以通过修改设置参数来定制Ideal Piano。



## 下载

你可以从[这里](https://www.jianguoyun.com/p/Daurwu0QhPG0CBjxt8QEIAA)下载这个软件的Windows, Linux和macOS版本。

注意1：对于Linux版本，使用默认设置播放MIDI文件需要安装freepats 和 timidity。然后按照使用须知里的步骤进行。在Ubuntu上，你可以运行

```
sudo apt-get install freepats timidity
```

如果你想在Linux版本中使用SoundFont文件作为乐器，你需要安装fluidsynth，你可以参考[这里](https://github.com/FluidSynth/fluidsynth/wiki/Download)了解不同Linux发行版的安装命令。对于Ubuntu，它是

```
sudo apt-get install fluidsynth
```

注意2：对于macOS版本，如果你想使用SoundFont文件作为乐器，你需要安装fluidsynth，你可以用homebrew在terminal运行这一行来安装fluidsynth

```
brew install fluidsynth
```



## 预览

以下是Ideal Piano的画面预览:

![image](previews/1.jpg)

<p align="center">打开Ideal Piano的初始页面</p


![image](previews/2.jpg)

<p align="center">显示你当前演奏的音符，分析和弦类型并显示在屏幕上
</p


![image](previews/3.jpg)

<p align="center">选择MIDI文件播放的窗口</p


![image](previews/4.jpg)

<p align="center">播放多轨的MIDI文件</p


![image](previews/5.jpg)

<p align="center">你可以直接拖拽图片文件到屏幕上改变背景</p>



## 从源代码构建

如果你不能在你目前的系统上运行可执行文件，最好的解决办法就是从源代码构建。

以Linux为例，由于一些核心库的差异和其他与新版本不兼容的问题，从Ubuntu 21.10构建的可执行文件可能无法在Ubuntu 22.04上运行。

有关如何从源代码构建Ideal Piano的信息，请查看`User Manual`文件夹中的使用须知。



## 其他说明

目前支持的语言只包括英语和中文，你可以通过改变设置参数`language`来改变语言。



## 捐赠

这个项目是由Rainbow Dreamer在业余时间开发的，旨在创建一个智能钢琴软件。如果你觉得这个项目对你有用，想支持它和它的未来发展，请考虑给我买杯咖啡，我很感激任何金额。

[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://www.paypal.com/donate/?business=7XSUZCQNT4M4Y&no_recurring=0&currency_code=CAD)



## 总结

如果你在使用本软件时遇到任何问题，请先看一下使用须知，如果你不能解决问题，请发邮件到 2180502841@qq.com 来联系我，感谢大家的支持~

