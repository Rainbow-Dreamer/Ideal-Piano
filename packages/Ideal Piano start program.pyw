import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.insert(0, abs_path)
sys.path.insert(0, 'packages')
import pygame
import pygame.midi
import time
import pyglet
from pyglet.window import key
import mido
import midiutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import py
import sf2_loader as rs
from pydub import AudioSegment
import browse
import musicpy as mp
from ast import literal_eval
with open('packages/config.py', encoding='utf-8-sig') as f:
    exec(f.read())

with open('packages/Ideal Piano.pyw', encoding='utf-8-sig') as f:
    exec(f.read())
