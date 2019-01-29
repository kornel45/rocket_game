from typing import Tuple, List

import pygame


def make_font(fonts: list, size: int) -> pygame.font.Font:
    """
    Method responsible for making font of certain size. You can specify name of font, then it will
    be searched in system fonts. If None then default font will be returned
    :param fonts: list of fonts
    :param size: size
    :return: pygame surface representing font
    """
    available = pygame.font.get_fonts()
    choices = map(lambda font: font.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}


def get_font(font_preferences: List[str], size: int) -> pygame.font.Font:
    """
    Method responsible for creating (if not already cached) and getting font surface
    :param font_preferences: font name
    :param size: font size
    :return: pygame surface representing font
    """
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font


_cached_text = {}


def create_text(text: str, fonts: list, size: int, color: Tuple[int, int, int]) -> pygame.Surface:
    """
    Method responsible for rendering image from pygame font surface
    :param text: text we want to show
    :param fonts: fonts we want to use (first available will be chosen)
    :param size: size of text
    :param color: color of text
    :return: image of a rendered pygame font
    """
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

