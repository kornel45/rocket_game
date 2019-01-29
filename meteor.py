import pygame
from typing import List


class Meteor:
    """
    Class represents meteors.
    """
    def __init__(self, x: int, y: int, x_acc: int, y_acc: int, rotation: int, rotation_counter: int, rotation_speed: int, rotation_direction: int, size: int):
        """
        Initializer of a Meteor class
        :param x: where to start to plot meteor on the x axis
        :param y: where to start to plot meteor on the y axis
        :param x_acc: horizontal speed of meteor
        :param y_acc: vertical speed of meteor
        :param rotation: actually angle of meteor; angle = 5 * rotation
        :param rotation_counter: counts when meteor should change rotation parameter
        :param rotation_speed: describe how much rotation_counter must equal to force change of rotation
        :param rotation_direction: describe in which direction meteor rotate: 1 is right, -1 is left
        :param size: radius of meteor in pixels
        """
        self.x = x
        self.y = y
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.rotation = rotation
        self.rotation_counter = rotation_counter
        self.rotation_speed = rotation_speed
        self.rotation_direction = rotation_direction
        self.size = size

    def is_visible(self, max_x: int, max_y: int) -> bool:
        """
        Check if meteor is in on the screen
        :param max_x: size of the x axis of screen
        :param max_y: size of the y axis of screen
        :return: is meteor visible or not
        """
        if self.x < - 2 * self.size or self.x > 1.2 * max_x or self.y < -2 * self.size or self.y > 1.2 * max_y:
            return False
        return True


def load_first_sprites_meteors(folder_path: str) -> List[pygame.Surface]:
    """
    Load sprites of meteors
    :param folder_path: folder to sprites
    :return list of images
    """
    meteors = []
    sizes = [70]
    position = [i for i in range(36)]
    for r in sizes:
        for p in position:
            name = "\\meteor_" + str(r) + "_" + str(p) + ".png"
            meteors.append(folder_path + name)
    return [pygame.image.load(x) for x in meteors]


def scaling(sprites: List[pygame.Surface], to_size: int) -> List[pygame.Surface]:
    """
    Scales images
    :param sprites: what it is scaling
    :param to_size: size of scaling in pixels
    :return: list of scaled images
    """
    return [pygame.transform.scale(picture, (to_size, to_size)) for picture in sprites]


def load_all_sprites_of_meteors(folder_path: str) -> List[List[pygame.Surface]]:
    """
    Load sprites of meteors and scales it.
    :return list of list, where each list contains scaled images
    """
    meteors70 = load_first_sprites_meteors(folder_path)
    meteors60 = scaling(meteors70, 120)
    meteors50 = scaling(meteors70, 100)
    meteors40 = scaling(meteors70, 80)
    meteors30 = scaling(meteors70, 60)
    return [meteors30, meteors40, meteors50, meteors60, meteors70]
