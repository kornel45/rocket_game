import os
import pygame

from background import Background
from game import Game
from meteor import load_sprites_meteors, sprites_of_meteor
from rocket import Rocket

x = 500
y = 40

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

if __name__ == '__main__':
    size = (1400, 1000)
    rocket = Rocket(0, 0, 60, 60, r'acc', r'no_acc')
    background = Background('background_image\\back1.jpg', (0, 0))
    game = Game(size, rocket, background, sprites_of_meteor)
    game.run()
    pygame.quit()
