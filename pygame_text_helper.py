# -*- coding: utf-8 -*-
"""
Module provides functionality of creating text accepted by pygame blit method
"""
import pygame


def make_font(fonts, size):
    available = pygame.font.get_fonts()
    choices = map(lambda font: font.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}


def get_font(font, size):
    global _cached_fonts
    key = str(font) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font, size)
        _cached_fonts[key] = font
    return font


_cached_text = {}


def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image


