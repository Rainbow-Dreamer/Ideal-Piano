import os
import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(abs_path)
sys.path.insert(0, abs_path)
sys.path.insert(0, 'packages')
import fractions
import pygame
import pygame.midi
import time
import pyglet
import mido_fix
from PyQt5 import QtGui, QtWidgets, QtCore
import py
from pydub import AudioSegment
from ast import literal_eval
from copy import deepcopy as copy
import importlib
import multiprocessing

with open('packages/Ideal Piano.pyw', encoding='utf-8') as f:
    exec(f.read())
