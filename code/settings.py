import pygame
import asyncio

from random import *
from os.path import join 
from os import walk
from math import *

pygame.init()
pygame.joystick.init()

global animals 
animals = [
    'Axolotl', 
    'Bat',
    'Bear',
    'Cat',
    'Crow',
    'Deer',
    'Dog',
    'Fox',
    'Frog',
    'Goat',
    'Hedgehog',
    'Penguin',
    'Rabbit',
    'Raccoon',
    'Wolf'
    ]

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
CHUNK_SIZE = 1024