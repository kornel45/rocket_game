import pygame


class Meteor:
    """
    Class represents meteors.
    """
    def __init__(self, x, y, x_acc, y_acc, rotation, rotation_counter, rotation_speed, rotation_direction, size):
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

    def is_visible(self, max_x, max_y):
        """
        Check if meteor is in on the screen
        :param max_x: size of the x axis of screen
        :param max_y: size of the y axis of screen
        :return:
        """
        if self.x < - 2 * self.size or self.x > 1.2 * max_x or self.y < -2 * self.size or self.y > 1.2 * max_y:
            return False
        return True


def load_first_sprites_meteors(folder_path):
    """
    Load sprites of meteors
    """
    meteors = []
    sizes = [70]
    position = [i for i in range(36)]
    for r in sizes:
        for p in position:
            nazwa = "\\meteor_" + str(r) + "_" + str(p) + ".png"
            meteors.append(folder_path + nazwa)
    return [pygame.image.load(x) for x in meteors]


def scaling(sprites, to_size):
    """
    Scales images
    :param sprites: what it is scaling
    :param to_size: size of scaling in pixels
    :return:
    """
    return [pygame.transform.scale(picture, (to_size, to_size)) for picture in sprites]


def load_all_sprites_of_meteors(folder_path):
    """
    Load sprites of meteors and scales it.
    """
    meteors70 = load_first_sprites_meteors(folder_path)
    meteors60 = scaling(meteors70, 120)
    meteors50 = scaling(meteors70, 100)
    meteors40 = scaling(meteors70, 80)
    meteors30 = scaling(meteors70, 60)
    return [meteors30, meteors40, meteors50, meteors60, meteors70]
