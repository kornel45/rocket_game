import math
import os

import pygame


class Rocket(pygame.Rect):
    def __init__(self, size_x, size_y, x, y, acc_sprites_folder, no_acc_sprites_folder):
        super(Rocket, self).__init__(size_x, size_y, x, y)
        self.acc_sprites = load_sprites(acc_sprites_folder)
        self.no_acc_sprites = load_sprites(no_acc_sprites_folder)
        self.hit_box = []
        self.sprites_len = len(self.acc_sprites)

    def get_image(self, acc, force, unlocked):
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

    def set_hit_box(self, sprite_num):
        self.hit_box = [(1,1) for i in range(8)]
        h=[(self.x + self.width // 2, self.y + self.height // 2) for i in range(8)]
        h2=[(math.cos((90 + i * 45) * math.pi / 180) * 15, math.sin((90 + i * 45) * math.pi / 180) * 35) for i in range(8)]
        a = - sprite_num / 10 + 55 * math.pi / 180
        for i in range(8):
            x, y = h2[i][0:2]
            self.hit_box[i] = int(y*math.sin(a) + x*math.cos(a) + h[i][0]), int(y*math.cos(a) - x*math.sin(a) + h[i][1])

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height




def load_sprites(folder_path):
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
