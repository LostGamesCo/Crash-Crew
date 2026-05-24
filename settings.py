import pygame
import pygame_light2d as pl2d
from pygame_light2d import LightingEngine, PointLight, Hull

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
screen_res = (1280, 720)
lights_engine = LightingEngine(
    screen_res=screen_res, native_res=screen_res, lightmap_res=(int(screen_res[0]/2.5), int(screen_res[1]/2.5)))