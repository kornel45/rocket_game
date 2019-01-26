# -*- coding: utf-8 -*-
"""
Module provides game itself
You can download needed sprites from here: https://www.mediafire.com/file/cb365fxtu8ivt2u/sprites.7z/file
"""
import math
import os
import random as r
from random import shuffle

import numpy
import pygame
from pygame.math import Vector2

from meteors import load_sprites_meteors
from rocket import load_sprites
from text_styler import create_text

x = 500
y = 40

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
colors = {
    'red': (255, 0, 0), 'black': (0, 0, 0),
    'white': (255, 255, 255), 'green': (0, 255, 0),
    'brown': (128, 0, 0), 'pink': (255, 51, 153),
    'yellow': (255, 255, 0), 'blue': (0, 0, 255),
    'purple': (153, 0, 255)
}


class Game:
    def __init__(self, size, rocket, sprites):
        self.game_option = [1, 0, 0, 0]  # wybory w opcjach, ale uwaga, to lista list
        self.sprites = sprites
        self.sprites_len = len(sprites[0])
        self.image = sprites[0][self.sprites_len // 2]
        self.max_x, self.max_y = size
        self.font = ["Comic Sans MS"]
        self.gravity = 10
        self.air_res = 0.8
        self.pos = None
        self.acc = None
        self.rocket = rocket
        self.clock = pygame.time.Clock()
        self.is_playing_game = False
        self.is_lost = False
        self.is_won = False
        self.move = 0.5
        self.tick_time = 60
        self.pause = False
        self.is_force = False
        self.background_color = colors['white']
        self.list_of_meteors = []
        self.main_menu_loop = True
        self.wind = 0

    def init_pos(self):
        self.pos = Vector2(self.max_x / 2, self.max_y / 4)

    def reset_acc(self):
        self.acc = Vector2(0, 0)

    def main_menu(self, screen):
        texts = ['Start game', 'Options', 'About', 'Exit']
        text_len = len(texts)
        option = 0
        while self.main_menu_loop:
            self.clock.tick(self.tick_time)
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
                            self.option_menu(screen)
                        elif option == 2:
                            self.about(screen)
                        elif option == 3:
                            self.main_menu_loop = False
                            self.is_playing_game = True
                    elif event.key == pygame.K_ESCAPE:
                        self.is_playing_game = True
                        self.main_menu_loop = False
                elif event.type == pygame.QUIT:
                    self.is_playing_game = True
                    self.main_menu_loop = False

            screen.fill(self.background_color)
            for i, text in enumerate(texts):
                if i == option:
                    color = (0, 155, 0)
                else:
                    color = (0, 0, 255)
                font_size = 60
                new_text = create_text(text, self.font, font_size, color)
                x_pos = (self.max_x - new_text.get_width()) // 2
                y_pos = (1 + i) * (self.max_y - new_text.get_height()) // (2 + text_len) + font_size
                screen.blit(new_text, (x_pos, y_pos))
            pygame.display.flip()

    def about(self, screen):
        is_about = True
        authors = ['Kornel Raczak', 'Pawel Gorecki', 'Lukasz Polakiewicz']
        shuffle(authors)
        texts = ['Authors:'] + authors + ['Press any key to escape...']
        text_len = len(texts)
        while is_about:
            self.clock.tick(self.tick_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_about = False
                    self.main_menu_loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                        is_about = False

            screen.fill(self.background_color)
            about_colors = [color for color in colors.values() if color != self.background_color]
            for i, text in enumerate(zip(texts, about_colors)):
                font_size = 60
                if text[0] == texts[-1]:
                    font_size = 30
                new_text = create_text(text[0], self.font, font_size, text[1])
                x_pos = (self.max_x - new_text.get_width()) // 2
                y_pos = (1 + i) * (self.max_y - new_text.get_height()) // (2 + text_len) + font_size
                screen.blit(new_text, (x_pos, y_pos))
            pygame.display.flip()

    def change_wind(self):
        if not self.game_option[3]:
            self.wind += (r.random() - 0.5) / 1000

    def set_wind_on_start(self):
        if self.game_option[2]:
            self.wind = 0.001  # r.random / 3

    def option_menu(self, screen):
        not_chosen = True
        option_meteors = ["Meteors: Easy", "Meteors: Medium", "Meteors: Hard", "Meteors: Impossible"]
        options1 = ['Music: Off', 'Music: On']
        options2 = ['Wind: On', 'Wind: Off']
        options3 = ['Wind: Constant', 'Wind: Unstable']
        options = [option_meteors, options1, options2, options3]
        game_option_len = []
        for option in options:
            game_option_len.append(len(option))
        option = 0
        text_len = len(options)
        while not_chosen:
            self.clock.tick(self.tick_time)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        option = (option + 1) % text_len
                    if event.key == pygame.K_UP:
                        option = (option - 1) % text_len
                    elif event.key == pygame.K_LEFT:
                        self.game_option[option] = (self.game_option[option] - 1) % game_option_len[option]
                    elif event.key == pygame.K_RIGHT:
                        self.game_option[option] = (self.game_option[option] + 1) % game_option_len[option]

                    elif event.key == pygame.K_ESCAPE:
                        not_chosen = False
                elif event.type == pygame.QUIT:
                    not_chosen = False
                    self.done = True

            screen.fill(self.background_color)
            for i, opt in enumerate(options):
                color = (0, 0, 255)
                font_size = 60
                what_to_write = opt[self.game_option[i]]
                if i == option:
                    color = (0, 255, 0)
                new_text = create_text(what_to_write, self.font, font_size, color)
                x_pos = (self.max_x - new_text.get_width()) // 2
                y_pos = (1 + i) * (self.max_y - new_text.get_height()) // (2 + text_len) + font_size
                screen.blit(new_text, (x_pos, y_pos))
            pygame.display.flip()

    def show_speed(self, screen):
        speed_x_val = abs(round(self.acc.x / (2 / 173)))
        speed_y_val = abs(round(self.acc.y / (2 / 173)))
        speed_x = create_text('Horizontal:  {} km/h'.format(speed_x_val), self.font, 20, (255, 0, 0))
        speed_y = create_text('Vertical:  {} km/h'.format(speed_y_val), self.font, 20, (255, 0, 0))
        speed_wind = create_text('Wind:  {} km/h'.format(round(10 * self.wind, 1)), self.font, 20, (255, 0, 0))
        screen.blit(speed_x, (10, 30))
        screen.blit(speed_y, (10, 10))
        screen.blit(speed_wind, (10, 50))

    def generate_surface(self, n, surface_length, rng):
        height = 1000
        width = 1400
        surf = []
        landing_site = [numpy.random.randint(surface_length, n - surface_length), height - numpy.random.randint(0, rng)]
        self.landing_site = [(landing_site[0] - surface_length) * width // n,
                             (landing_site[0] + surface_length) * width // n]
        for i in range(n):
            if abs(i - landing_site[0]) <= surface_length:
                surf.append([i * width // n, landing_site[1]])
            else:
                surf.append((i * width // n, height - numpy.random.randint(0, rng)))
        surf.append((width - 1, height))
        self.surface = [0] * width
        for i in range(n):
            for j in range(width // n):
                self.surface[i * width // n + j] = (surf[i][1] * (width // n - j) + surf[i + 1][1] * j) // (width // n)
        return surf

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.max_x, self.max_y))
        self.main_menu(screen)

    def reset_meteors(self):
        self.list_of_meteors = []

    def pause_game(self, screen):
        game_pause = create_text("Game Pause", self.font, 90, colors['red'])
        pause_menu = True
        while pause_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pause_menu = False
            self.show_text(screen, game_pause, 1 / 2, 1 / 4)
            pygame.display.flip()
            self.clock.tick(30)

    def play_game(self, screen):
        self.is_playing_game = True
        self.init_pos()
        self.reset_acc()
        self.reset_meteors()
        planet_surface = self.generate_surface(100, 5, 500)
        self.set_wind_on_start()
        while self.is_playing_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.pause_game(screen)
            pressed = pygame.key.get_pressed()
            if self.prob_of_new_meteor():
                self.add_meteor()
            self.change_wind()
            self.change_acc(pressed)
            self.add_gravity()
            self.add_air_resistance()
            self.add_wind()
            self.change_rocket_position()
            screen.fill(self.background_color)
            pygame.draw.lines(screen, 0, 0, planet_surface, 10)
            self.draw_meteors(screen)
            self.draw_rocket(screen)
            self.show_speed(screen)
            self.is_game_lost()

            if self.is_lost:
                if self.game_option[1]:
                    s = pygame.mixer.Sound('death.wav')
                    s.play()
                self.game_over(screen)
                self.reset_meteors()
            if self.is_won:
                if self.game_option[1]:
                    s = pygame.mixer.Sound('victory.wav')
                    s.play()
                self.game_won(screen)
                self.reset_meteors()
            pygame.display.flip()
            self.clock.tick(self.tick_time)

    def prob_of_new_meteor(self):
        liczniki = [0.01, 0.03, 0.06, 0.1]
        return r.random() < liczniki[self.game_option[0]]

    def draw_meteors(self, screen):
        for i, meteor in enumerate(self.list_of_meteors):
            self.list_of_meteors[i].x += meteor.x_acc - self.wind
            self.list_of_meteors[i].y += meteor.y_acc
            self.list_of_meteors[i].rotation_counter = (meteor.rotation_counter + 1) % meteor.rotation_speed
            if self.list_of_meteors[i].rotation_counter == 0:
                self.list_of_meteors[i].rotation = (meteor.rotation + 1) % 36
            scale_size = {70: -1, 60: -2, 50: -3, 40: -4, 30: -5}
            image_meteor = self.sprites[scale_size[meteor.size]][meteor.rotation]
            self.meteor = pygame.Rect(meteor.x, meteor.y, image_meteor.get_width(), image_meteor.get_height())
            screen.blit(image_meteor, self.meteor)

    def add_meteor(self):
        brzeg = 100
        if r.random() < 0.8:
            y = -brzeg
            x = r.random() * self.max_x
            x_acc = r.random() * 2 - 4
            y_acc = r.random() * 2 + 1
        else:
            if r.random() < 0.5:
                y = r.random() * self.max_y / 3
                x = self.max_x + brzeg
                x_acc = - r.random() * 2
                y_acc = r.random() * 2 - 1
            else:
                y = r.random() * self.max_y / 3
                x = -brzeg
                x_acc = r.random() * 2
                y_acc = r.random() * 2 - 1
        rotation = 0
        rotation_speed = r.randint(1, 3)
        rotation_counter = 0
        size = r.choice([70, 60, 50, 40, 30])
        meteor = Meteor(x, y, x_acc, y_acc, rotation, rotation_counter, rotation_speed, size)
        self.list_of_meteors.append(meteor)

    def is_game_lost(self):
        if not 0 < self.rocket.x < self.max_x - self.rocket.width:
            self.is_lost = True
        if not 0 < self.rocket.y < self.max_y - self.rocket.height:
            self.is_lost = True
        if not self.rocket.y <= self.surface[self.rocket.x] - self.rocket.height:
            if abs(self.acc.x) + abs(self.acc.y) < 4 and self.landing_site[0] < self.rocket.x < self.landing_site[1]:
                self.is_won = True
            else:
                self.is_lost = True
        self.meteors_collision()

    def meteors_collision(self):
        for meteor in self.list_of_meteors:
            for x, y in self.hitbox:
                if ((meteor.x + meteor.size) - x) ** 2 + ((meteor.y + meteor.size) - y) ** 2 <= 0.81 * meteor.size ** 2:
                    self.is_lost = True

    def draw_rocket(self, screen):
        n = 24
        sprite_num = int(round(self.acc.x * n / self.sprites_len)) + self.sprites_len // 2
        if sprite_num >= self.sprites_len - 1:
            sprite_num = self.sprites_len - 1
        elif sprite_num < 0:
            sprite_num = 0
        self.image = self.sprites[self.is_force][sprite_num]
        self.rocket = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())
        self.hitbox = [
            (self.rocket.x + self.rocket.width // 2 + math.cos((90 - sprite_num + i * 45) * math.pi / 180) * 15,
             self.rocket.y + self.rocket.height // 2 + math.sin((90 - sprite_num + i * 45) * math.pi / 180) * 35)
            for i in range(8)]
        screen.blit(self.image, self.rocket)

    def change_rocket_position(self):
        if not self.pause:
            self.pos += self.acc

    def add_air_resistance(self):
        if not self.pause:
            self.acc *= (1 - self.air_res / self.tick_time)

    def add_gravity(self):
        if not self.pause:
            self.acc.y += self.gravity / self.tick_time

    def add_wind(self):
        self.acc.x -= self.wind

    def change_acc(self, pressed):
        self.pause = False
        self.is_force = False
        if pressed[pygame.K_UP]:
            self.acc.y -= self.move
            self.is_force = True
        if pressed[pygame.K_DOWN]:
            if self.acc.y < 0:
                self.acc.y = min(0, self.acc.y + self.move // 4)
        if pressed[pygame.K_LEFT]:
            self.acc.x -= self.move / 2
        if pressed[pygame.K_RIGHT]:
            self.acc.x += self.move / 2
        if pressed[pygame.K_SPACE]:
            self.pause = True

    def show_text(self, screen, text, x_ratio, y_ratio):
        x_pos = x_ratio * (self.max_x - text.get_width())
        y_pos = y_ratio * (self.max_y - text.get_height())
        screen.blit(text, (x_pos, y_pos))

    def game_over(self, screen):
        while self.is_lost:
            game_over_text = create_text("Game Over", self.font, 110, (255, 0, 0))
            continue_text = create_text("Press space to restart game", self.font, 35, (255, 0, 0))
            back_to_menu = create_text("Press escape to back to menu", self.font, 35, (255, 0, 0))

            self.show_text(screen, game_over_text, 1 / 2, 1 / 4)
            self.show_text(screen, continue_text, 1 / 2, 4 / 11)
            self.show_text(screen, back_to_menu, 1 / 2, 5 / 11)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_lost = False
                        self.init_pos()
                        self.reset_acc()
                        self.reset_meteors()
                    elif event.key == pygame.K_ESCAPE:
                        self.is_lost = False
                        self.is_playing_game = False
            self.clock.tick(self.tick_time)

    def game_won(self, screen):
        while self.is_won:
            game_over_text = create_text("You won!", self.font, 110, (128, 128, 0))
            continue_text = create_text("Press space to restart game", self.font, 35, (128, 128, 0))
            back_to_menu = create_text("Press escape to back to menu", self.font, 35, (128, 128, 0))

            self.show_text(screen, game_over_text, 1 / 2, 1 / 4)
            self.show_text(screen, continue_text, 1 / 2, 4 / 11)
            self.show_text(screen, back_to_menu, 1 / 2, 5 / 11)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_won = False
                        self.init_pos()
                        self.reset_acc()
                    elif event.key == pygame.K_ESCAPE:
                        self.is_won = False
                        self.is_playing_game = False
            self.clock.tick(self.tick_time)


class Meteor:
    def __init__(self, x, y, x_acc, y_acc, rotation, rotation_counter, rotation_speed, size):
        self.x = x
        self.y = y
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.rotation = rotation
        self.rotation_counter = rotation_counter
        self.rotation_speed = rotation_speed
        self.size = size


if __name__ == '__main__':
    size = (1400, 1000)
    rocket = pygame.Rect(size[0] / 2, size[1] / 2, 60, 60)
    sprites_no_acc = load_sprites(r'no_acc')
    sprites_acc = load_sprites(r'acc')
    meteor = pygame.image.load(r'meteors\kometa.png')
    meteors70 = load_sprites_meteors(r'meteors')
    meteors60 = [pygame.transform.scale(picture, (120, 120)) for picture in meteors70]
    meteors50 = [pygame.transform.scale(picture, (100, 100)) for picture in meteors70]
    meteors40 = [pygame.transform.scale(picture, (80, 80)) for picture in meteors70]
    meteors30 = [pygame.transform.scale(picture, (50, 50)) for picture in meteors70]
    sprites = [sprites_no_acc, sprites_acc, meteors30, meteors40, meteors50, meteors60, meteors70]
    game = Game(size, rocket, sprites)
    game.run()
    pygame.quit()
