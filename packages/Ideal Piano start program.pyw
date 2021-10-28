import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.append(abs_path)
sys.path.append('packages')
import pygame
import pygame.midi
import keyboard
import time
import pyglet
import mido
import midiutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

with open('packages/musicpy/__init__.py', encoding='utf-8-sig') as f:
    exec(f.read())
os.chdir(abs_path)
with open('packages/config.py', encoding='utf-8-sig') as f:
    exec(f.read())
with open('packages/browse.py', encoding='utf-8-sig') as f:
    exec(f.read())
with open('packages/Ideal Piano.pyw', encoding='utf-8-sig') as f:
    exec(f.read())
