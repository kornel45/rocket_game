"""
Module provides game itself
"""
import math
import os

import pygame
from pygame.math import Vector2

from pygame_text_helper import create_text

x = 40
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

font_preferences = ["Papyrus", "Comic Sans MS"]


class Game:
    def __init__(self, size, rocket):
        self.max_x, self.max_y = size
        self.gravity = 3
        self.air_res = 0.9
        self.pos = None
        self.acc = None
        self.rocket = rocket
        self.clock = pygame.time.Clock()
        self.done = False
        self.lost_game = True
        self.move = 0.5
        self.tick_time = 60

    def init_pos(self):
        self.pos = Vector2(self.max_x / 2, self.max_y / 2)

    def reset_acc(self):
        self.acc = Vector2(0, 0)

    def main_menu(self, screen):
        not_chosen = True
        texts = ['Start game', 'Options', 'Exit']
        text_len = len(texts)
        option = 0
        while not_chosen:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        option = (option + 1) % text_len
                    elif event.key == pygame.K_UP:
                        option = (option - 1) % text_len
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if option == 0:
                            self.play_game(screen)
                        elif option == 1:
                            self.option_menu()
                        elif option == 2:
                            not_chosen = False
                            self.done = True
                    elif event.key == pygame.K_ESCAPE:
                        self.done = True
                        not_chosen = False
                elif event.type == pygame.QUIT:
                    self.done = True
                    not_chosen = False

            screen.fill((0, 0, 0))
            for i, text in enumerate(texts):
                if i == option:
                    color = (0, 155, 0)
                else:
                    color = (0, 0, 255)
                font_size = 60
                new_text = create_text(text, font_preferences, font_size, color)
                x_pos = (self.max_x - new_text.get_width()) // 2
                y_pos = (1 + i) * (self.max_y - new_text.get_height()) // (2 + text_len) + font_size
                screen.blit(new_text, (x_pos, y_pos))

            pygame.display.flip()
            self.clock.tick(12)

    def option_menu(self):
        pass

    def show_speed(self, screen):
        speed = round(math.sqrt(self.acc.x ** 2 + self.acc.y ** 2) / (2 / 173))
        speed = create_text('{} km/h'.format(speed), font_preferences, 20, (255, 0, 0))
        screen.blit(speed, (10, 10))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.max_x, self.max_y))
        self.main_menu(screen)

    def play_game(self, screen):
        self.done = False
        self.init_pos()
        self.reset_acc()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pressed = pygame.key.get_pressed()
            self.change_acc(pressed)
            self.add_gravity()
            self.add_air_resistance()
            self.change_rocket_position()
            screen.fill((0, 0, 0))
            self.draw_rocket(screen)
            self.show_speed(screen)
            self.game_over(screen)
            pygame.display.flip()
            self.clock.tick(self.tick_time)

    def is_game_lost(self):
        if not 0 < self.rocket.x < self.max_x - self.rocket.width:
            self.lost_game = False
        if not 0 < self.rocket.y < self.max_y - self.rocket.height:
            self.lost_game = False

    def draw_rocket(self, screen):
        self.rocket = pygame.Rect(self.pos.x, self.pos.y, 60, 60)
        pygame.draw.rect(screen, (0, 128, 255), self.rocket)
        # screen.blit(self.image, self.rocket)

    def change_rocket_position(self):
        self.pos += self.acc

    def add_air_resistance(self):
        self.acc *= (1 - self.air_res / self.tick_time)

    def add_gravity(self):
        self.acc.y += self.gravity / self.tick_time

    def change_acc(self, pressed):
        if pressed[pygame.K_UP]:
            self.acc.y -= self.move
        if pressed[pygame.K_DOWN]:
            self.acc.y += self.move
        if pressed[pygame.K_LEFT]:
            self.acc.x -= self.move / 2
        if pressed[pygame.K_RIGHT]:
            self.acc.x += self.move / 2

    def show_text(self, screen, text, x_ratio, y_ratio):
        x_pos = x_ratio * (self.max_x - text.get_width())
        y_pos = y_ratio * (self.max_y - text.get_height())
        screen.blit(text, (x_pos, y_pos))

    def game_over(self, screen):
        self.is_game_lost()
        while not self.lost_game:
            game_over_text = create_text("Game Over", font_preferences, 110, (255, 0, 0))
            continue_text = create_text("Press space to restart game", font_preferences, 35, (255, 0, 0))
            back_to_menu = create_text("Press escape to back to menu", font_preferences, 35, (255, 0, 0))

            self.show_text(screen, game_over_text, 1 / 2, 1 / 2)
            self.show_text(screen, continue_text, 1 / 2, 7 / 11)
            self.show_text(screen, back_to_menu, 1 / 2, 8 / 11)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.lost_game = True
                        self.init_pos()
                        self.reset_acc()
                    elif event.key == pygame.K_ESCAPE:
                        self.lost_game = True
                        self.done = True


if __name__ == '__main__':
    size = (1400, 1000)
    rocket = pygame.Rect(size[0] / 2, size[1] / 2, 60, 60)
    game = Game(size, rocket)
    game.run()
