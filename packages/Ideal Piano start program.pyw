import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.insert(0, abs_path)
sys.path.insert(0, 'packages')
sys.path.append('tools')
import pygame
import pygame.midi
import time
import pyglet
import mido
import midiutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import py
from pydub import AudioSegment
import browse
import musicpy as mp
from ast import literal_eval
import piano_config
from change_settings import config_window
from copy import deepcopy as copy
import importlib

with open('packages/Ideal Piano.pyw', encoding='utf-8-sig') as f:
    exec(f.read())
