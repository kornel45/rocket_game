# -*- coding: utf-8 -*-
"""
Module provides functionality of creating text accepted by pygame blit method
"""
import pygame


def make_font(fonts, size):
    """
    Method responsible for making font of certain size. You can specify name of font, then it will
    be searched in system fonts. If None then default font will be returned
    :param fonts: list of fonts
    :type fonts: list or None
    :param size: size
    :type size: int
    :return: pygame surface representing font
    :rtype: pygame.font.Font
    """
    available = pygame.font.get_fonts()
    choices = map(lambda font: font.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}


def get_font(font, size):
    """
    Method responsible for creating (if not already cached) and getting font surface
    :param font: font name
    :param size: font size
    :return: pygame surface representing font
    rtype: pygame.font.Font
    """
    global _cached_fonts
    key = str(font) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font, size)
        _cached_fonts[key] = font
    return font


_cached_text = {}


def create_text(text, fonts, size, color):
    """
    Method responsible for rendering image from pygame font surface
    :param text: text we want to show
    :type text: str
    :param fonts: fonts we want to use (first available will be choosen)
    :type fonts: list
    :param size: size of text
    :type size: int
    :param color: color of text
    :type color: str
    :return: image of a rendered pygame font
    :rtype: pygame.image
    """
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image


