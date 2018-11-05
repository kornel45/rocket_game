import os
import pygame


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
