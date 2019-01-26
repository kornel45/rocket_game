# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 17:06:37 2019

@author: polakiew
"""
import pygame


def load_sprites_meteors(folder_path):
    meteory = []
    rozmiary = [70]
    pozycje = [i for i in range(36)]
    for r in rozmiary:
        for p in pozycje:
            nazwa = "\\meteor_" + str(r) + "_" + str(p) + ".png"
            meteory.append(folder_path + nazwa)

    return [pygame.image.load(x) for x in meteory]
