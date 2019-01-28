import os
import pygame

from background import Background
from game import Game
from meteor import load_sprites_meteors
from rocket import Rocket

x = 500
y = 40

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

if __name__ == '__main__':
    size = (1400, 1000)

    # do przerobienia #############################################################
    meteor = pygame.image.load(r'meteors\kometa.png')
    meteors70 = load_sprites_meteors(r'meteors')
    meteors60 = [pygame.transform.scale(picture, (120, 120)) for picture in meteors70]
    meteors50 = [pygame.transform.scale(picture, (100, 100)) for picture in meteors70]
    meteors40 = [pygame.transform.scale(picture, (80, 80)) for picture in meteors70]
    meteors30 = [pygame.transform.scale(picture, (60, 60)) for picture in meteors70]
    sprites = [meteors30, meteors40, meteors50, meteors60, meteors70]
    ###############################################################################
    rocket = Rocket(0, 0, 60, 60, r'acc', r'no_acc')
    background = Background('background_image\\back1.jpg', (0, 0))
    game = Game(size, rocket, background, sprites)
    game.run()
    pygame.quit()
