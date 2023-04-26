import os.path

import pygame as pg
import random


# define colors, colors work in a (RGB) format.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_PURPLE = (200,0,200)
PURPLE = (128,0,128)
YELLOW = (255,255,0)
TEAL = (0,255,255)
PINK = (255,0,255)
ORANGE = (255,127,0)
DARK_GRAY = (64,64,64)
LIGHT_GRAY = (192,192,192)
GRAY_BLUE = (92,192,194)

colors = (WHITE,BLUE,BLACK,RED,GREEN,YELLOW,TEAL,PINK,ORANGE)



#Game Title
TITLE = "Celestial Corruption"



# Window Settings
WIDTH = 1280
HEIGHT = 920
DEFAULT_COLOR = BLACK
TILE_SIZEX = WIDTH/15
TILE_SIZEY = HEIGHT/15


GRAV_MOD = 0.75
GLIDE_MOD = 2 #doesn't apply multiple times, purely is the amount going down


# camera settings
fps = 60

# file locations
#gets location of file on computer
game_folder = os.path.dirname(__file__)
game_folder = game_folder.replace("\scripts","")
sprites_folder = os.path.join(game_folder,"sprites")
playerSprites = os.path.join(sprites_folder,"playerSprites")
enemySprites = os.path.join(sprites_folder,"enemySprites")
background_folder = os.path.join(sprites_folder, "Background")
background_image = os.path.join(background_folder, "Background.png")
alt_background_image = os.path.join(background_folder, "nicesky.png")

snd_folder = os.path.join(game_folder, "snd")
music_snd_folder = os.path.join(snd_folder,'music')
MAIN_THEME = os.path.join(music_snd_folder, "the_ritual.ogg")
TITLE_THEME = os.path.join(music_snd_folder, 'sinister_abode.wav')
soundfx_folder = os.path.join(snd_folder,'soundfx')
bullet_sound = os.path.join(soundfx_folder,'bullet_sound.wav')
CONFIRM_SOUND = os.path.join(soundfx_folder,'Confirm.wav')
enemy_death_sound = os.path.join(soundfx_folder,'enemyDeath.wav')
player_death_sound = os.path.join(soundfx_folder,'playerDeath.wav')


platform_image = os.path.join(background_folder,"platform.png")

highScores = 'highscores.txt'
HS_FILE = os.path.join(game_folder, highScores)

# player Settings

bullet_sprite = os.path.join(playerSprites,"jewerlery.png")
player_sprite = os.path.join(playerSprites, "Player.png")
player_wings = os.path.join(playerSprites,'Player_wings.png')

PLAYER_ACC = 0.85
PLAYER_FRICTION = -0.12
PLAYER_JUMP = 20


# Enemy Settings
enemy_cloud = os.path.join(enemySprites, "StormCloudEnemy.png")
ENEMY_SPEED = 0.35


#Platforms
 #                      x               y               Width,Height, trasnparency  (true)
PLATFORM_CONFIG_1 = [(WIDTH / 2 - 340, HEIGHT * 3 / 4 - 10, 420, 30, True), # Lowest Plat
                     (WIDTH / 3 + 440, HEIGHT * 3 / 6 + 60, 300, 30, True), # Right Mid
                     (WIDTH / 3 - 500, HEIGHT * 3 / 6 + 50, 300, 30, True), # Left Mid
                     (WIDTH / 3 + 200, HEIGHT * 2 / 8 + 58, 300, 30, True), # Right top
                     (WIDTH / 3 - 200, HEIGHT * 2 / 8, 300, 30, True)] # Left Top



