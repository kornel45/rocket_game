""" Main module of a game. This is where main settings are set """
import os
import pygame

from background import Background
from game import Game
from meteor import load_all_sprites_of_meteors
from rocket import Rocket

x = 500
y = 40

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

if __name__ == '__main__':
    size = (1400, 1000)
    rocket = Rocket(0, 0, 60, 60, r'acc', r'no_acc')
    background = Background('background_image\\back1.jpg', (0, 0))
    sprites_of_meteor = load_all_sprites_of_meteors(r'meteors')
    game = Game(size, rocket, background, sprites_of_meteor)
    game.run()
    pygame.quit()
