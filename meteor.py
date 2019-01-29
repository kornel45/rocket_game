import pygame


class Meteor:
    def __init__(self, x, y, x_acc, y_acc, rotation, rotation_counter, rotation_speed, rotation_direction, size):
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
        if self.x < - 2 * self.size or self.x > 1.2 * max_x or self.y < -2 * self.size or self.y > 1.2 * max_y:
            return False
        return True


def load_sprites_meteors(folder_path):
    meteory = []
    rozmiary = [70]
    pozycje = [i for i in range(36)]
    for r in rozmiary:
        for p in pozycje:
            nazwa = "\\meteor_" + str(r) + "_" + str(p) + ".png"
            meteory.append(folder_path + nazwa)
    return [pygame.image.load(x) for x in meteory]

def scaling(sprites, to_size):
    return [pygame.transform.scale(picture, (to_size, to_size)) for picture in sprites]

meteors70 = load_sprites_meteors(r'meteors')
meteors60 = scaling(meteors70, 120)
meteors50 = scaling(meteors70, 100)
meteors40 = scaling(meteors70, 80)
meteors30 = scaling(meteors70, 60)
sprites_of_meteor = [meteors30, meteors40, meteors50, meteors60, meteors70]
