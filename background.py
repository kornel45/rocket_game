""" Module provides class that handles background image """
from typing import Tuple

import pygame


class Background(pygame.sprite.Sprite):
    """ Class responsible for providing background image """

    def __init__(self, image_file: str, location: Tuple[int, int] = (0, 0)):
        """
        Initializer of a class
        :param image_file: absolute path to image
        :param location: (x, y) where to start image, default x=0, y=0
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
