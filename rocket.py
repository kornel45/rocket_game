""" Module provides Rocket class which is representing Rocket in game """
import math
import os
from typing import List

import pygame


class Rocket(pygame.Rect):
    """ Rocket class, based on pygame.Rect. Possible customization is with size and graphics look """

    def __init__(self, x: int, y: int, width: int, height: int, acc_sprites_folder: str, no_acc_sprites_folder: str):
        """
        Initializer of a Rocket class
        :param x: where to start to plot rocket on the x axis
        :param y: where to start to plot rocket on the y axis
        :param width: width of a rocket
        :param height: height of a rocket
        :param acc_sprites_folder: path to folder with acceleration sprites
        :param no_acc_sprites_folder: path to folder without acceleration sprites
        """
        super(Rocket, self).__init__(x, y, width, height)
        self.acc_sprites = load_sprites(acc_sprites_folder)
        self.no_acc_sprites = load_sprites(no_acc_sprites_folder)
        self.hit_box = []
        self.sprites_len = len(self.acc_sprites)

    def get_image(self, acc: pygame.Vector2, force: bool, unlocked: bool) -> pygame.image:
        """
        Returns image of a rocket corresponding to it's speed in vertical and horizontal direction.
        Also it looks at if player holds Up Arrow button (force) and if the game already started (unlocked)
        :param acc: vector of acceleration
        :param force: if player presses up arrow
        :param unlocked: if game already started
        :return: image of a rocket
        """
        n = 24
        sprite_num = int(round(acc.x * n / self.sprites_len)) + self.sprites_len // 2
        if sprite_num >= self.sprites_len - 1:
            sprite_num = self.sprites_len - 1
        elif sprite_num < 0:
            sprite_num = 0
        self.set_hit_box(sprite_num)
        if force and unlocked:
            return self.acc_sprites[sprite_num]
        else:
            return self.no_acc_sprites[sprite_num]

    def set_hit_box(self, sprite_num: int):
        """
        Method calculates current hit box based on sprite currently drawn
        :param sprite_num: sprite number
        """
        self.hit_box = [(1, 1) for i in range(8)]
        h = [(self.x + self.width // 2, self.y + self.height // 2) for i in range(8)]
        h2 = [(math.cos((90 + i * 45) * math.pi / 180) * 15, math.sin((90 + i * 45) * math.pi / 180) * 35) for i in
              range(8)]
        a = - sprite_num / 10 + 55 * math.pi / 180
        for i in range(8):
            x, y = h2[i][0:2]
            self.hit_box[i] = int(y * math.sin(a) + x * math.cos(a) + h[i][0]), int(
                y * math.cos(a) - x * math.sin(a) + h[i][1])

    def set_pos(self, x: int, y: int):
        """
        Sets position of a rocket
        :param x:
        :param y:
        :return:
        """
        self.x = x
        self.y = y

    def set_width(self, width: int):
        """ Sets width of a rocket """
        self.width = width

    def set_height(self, height: int):
        """ Sets height of a rocket """
        self.height = height


def load_sprites(folder_path: str) -> List[pygame.Surface]:
    """
    Method loads sprites from folder_path
    :param folder_path: path to folder containing rocket sprites
    :return: list of rocket sprites
    """
    left = []
    right = []
    for pic_name in sorted(os.listdir(folder_path)):
        pic_path = os.path.join(folder_path, pic_name)
        if 'left' in pic_path:
            left.append(pic_path)
        elif 'right' in pic_path:
            right.append(pic_path)
        elif 'start' in pic_path:
            start = pic_path
    left = sorted(left, key=lambda x: int(x[-6:-4]), reverse=True)
    right = sorted(right, key=lambda x: int(x[-6:-4]))
    left.append(start)
    left.extend(right)
    return [pygame.image.load(x) for x in left]
