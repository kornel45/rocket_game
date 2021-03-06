# -*- coding: utf-8 -*-
"""
Module provides game itself. \n
It is enough to execute main to get game working\n
"""

import random as r
import time
from random import shuffle
from typing import List

import numpy
import pygame
from pygame.math import Vector2
from scipy.interpolate import interp1d

from background import Background
from meteor import Meteor
from rocket import Rocket
from text_styler import create_text

colors = {
    'red': (255, 0, 0), 'black': (0, 0, 0),
    'white': (255, 255, 255), 'green': (0, 255, 0),
    'brown': (128, 0, 0), 'pink': (255, 51, 153),
    'yellow': (255, 255, 0), 'blue': (0, 0, 255),
    'purple': (153, 0, 255)
}


class Game:
    """ Main module responsible for initialization and handling game itself """
    def __init__(self, size: tuple, rocket: Rocket, background: Background, sprites: List[List[pygame.Surface]]):
        """
        Initializer of a Game class
        :param size: size of game window
        :type size: tuple
        :param rocket: Rect object representing rocket
        :param sprites: list of images representing rocket look
        """
        self.max_x, self.max_y = size
        self.rocket = rocket
        self.background = background
        self.sprites = sprites
        self.game_option = [1, 0, 0, 0]
        self.font = ["Comic Sans MS"]
        self.gravity = 10
        self.air_res = 0.8
        self.pos = None
        self.acc = None
        self.clock = pygame.time.Clock()
        self.move = 0.5
        self.tick_time = 60
        self.background_color = colors['white']
        self.list_of_meteors = []
        self.wind = 0
        self.maximum_number_of_meteors = 20
        self.main_menu_loop = True
        self.is_playing_game = False
        self.game_started = False
        self.is_force = False
        self.is_lost = False
        self.is_won = False
        self.pause = False
        self.win_time = time.time()
        self.count_down_time = 2

    def init_pos(self):
        """
        Method used to initialize rocket position
        """
        self.pos = Vector2(self.start_position, self.surface[self.start_position] - 69)
        self.rocket.x, self.rocket.y = self.pos

    def reset_acc(self):
        """
        Method responsible for resetting acceleration of a rocket
        """
        self.acc = Vector2(0, 0)

    def main_menu(self, screen: pygame.Surface):
        """
        This creates main menu while loop. It's actually the main windows of the game.
        :param screen: Screen on which main menu should be displayed
        """
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
                            self.about_menu(screen)
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

    def about_menu(self, screen: pygame.Surface):
        """
        Menu option showing authors of this marvelous game
        :param screen: about menu will be shown on specified screen
        """
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
        """ Method responsible for changing the force of wind"""
        if self.game_option[3] and not self.game_option[2]:
            self.wind += (r.random() - 0.5) / 700

    def set_wind_on_start(self):
        """ Initializes wind force at the beginning of a game"""
        if not self.game_option[2]:
            self.wind = (r.random() * 2 - 1) / 100

    def set_maximum_number_of_meteors(self):
        """ Sets max number of meteors shown on display """
        self.maximum_number_of_meteors = 12 + 4 * self.game_option[0]

    def option_menu(self, screen: pygame.Surface):
        """
        Creates option menu, where user can configure game play
        :param screen: Screen on which main menu should be displayed
        """
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
                    self.main_menu_loop = False

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

    def show_speed(self, screen: pygame.Surface):
        """
        Method responsible for showing vertical and horizontal speed of rocket, but also the speed of wind.
        :param screen: Screen on which above speeds will be shown
        """
        lagrangian = 117 / 17
        speed_x_val = abs(round(self.acc.x * lagrangian))
        speed_y_val = abs(round(self.acc.y * lagrangian))
        wind = abs(round(self.wind * lagrangian))
        if self.wind > 0:
            wind_direction = ' <-'
        else:
            wind_direction = ' ->'
        speed_x = create_text('Horizontal:  {} m/h'.format(speed_x_val), self.font, 20, (255, 0, 0))
        speed_y = create_text('Vertical:  {} m/h'.format(speed_y_val), self.font, 20, (255, 0, 0))
        speed_wind = create_text('Wind:' + wind_direction + ' {} m/h'.format(10 * wind), self.font, 20, (255, 0, 0))
        screen.blit(speed_x, (10, 30))
        screen.blit(speed_y, (10, 10))
        screen.blit(speed_wind, (10, 50))

    def generate_surface(self, rng: int):
        """
        Generates planet surface along with landing platforms.
        :param rng: Sets maximum height of planets' surface
        """
        self.surface = [self.max_y - 10] * self.max_x
        self.landing_site = []
        self.prepend = 100
        self.site_size = 150
        for i in range(500):
            main_terrain = numpy.random.randint(700, 900)
            self.surface += self.generate_main_terrain(main_terrain, rng, self.surface[self.prepend - 1])
            self.surface += [self.surface[-1]] * self.site_size
            self.landing_site += [
                [self.prepend + self.site_size + main_terrain, self.prepend + 2 * self.site_size + main_terrain]]
        self.start_position = self.prepend + self.site_size // 2 - self.rocket.width // 8
        self.surface = self.surface[(self.max_x - self.prepend - self.site_size):]
        self.cutscene()

    def fill_surface(self, screen: pygame.Surface):
        """
        Fills surface with colour.
        :param screen: Screen on which surface is drawn
        """
        for x in range(0, self.max_x, 3):
            pygame.draw.line(screen, (x // 10 % 256, x // 40 % 256, (x // 20 + 20) % 256), [x, self.max_y],
                             [x, self.surface[x]], 5)

    def cutscene(self):
        """ Moves surface to the right to enable landing on yet another platform. """
        self.surface = self.surface[(self.landing_site[0][0] - self.prepend):]
        self.landing_site = self.landing_site[1:]

    def generate_main_terrain(self, main_terrain: int, rng: int, start: int) -> List[int]:
        """
        Generates curve of terrain in between two platforms.
        :param main_terrain: length of terrain to be generated
        :param rng: maximum height of terrain to be generated
        :param start: heigt of platform preceeding generated piece of terrain
        """
        x = numpy.linspace(0, main_terrain, 20)
        y = [self.max_y - numpy.random.randint(10, rng) for i in range(20)]
        f = interp1d(x, y, kind='cubic')
        return list(f(range(main_terrain)))

    def run(self):
        """ Main method of a Game class. It's responsible for initialization of pygame module and main_menu method. """
        pygame.init()
        pygame.display.set_caption('Mathematicians into space')
        path = r'icon.png'
        icon = pygame.image.load(path)
        icon.set_colorkey((0, 255, 0))
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode((self.max_x, self.max_y))
        self.background.image = self.background.image.convert()
        self.main_menu(screen)

    def reset_meteors(self):
        """ Clears space from meteors and adds some meteors on start"""
        self.list_of_meteors = []
        how_much_on_start = [6, 9, 12, 15]
        for i in range(how_much_on_start[self.game_option[0]]):
            self.add_meteor()

    def reset_wind(self):
        """ Resets wind """
        self.wind = 0

    def pause_game(self, screen: pygame.Surface):
        """
        Pauses game, so that player can go for a drink
        :param screen: Screen on which main menu should be displayed
        """
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

    def play_game(self, screen: pygame.Surface):
        """
        Turns on window with game play itself. This method is responsible for all the fun you have!
        :param screen: Screen on which main menu should be displayed
        """
        self.is_playing_game = True
        self.generate_surface(0.5 * self.max_y)
        self.reset_stage()
        self.set_maximum_number_of_meteors()

        counting_texts = [create_text(text, self.font, 165, colors['red']) for text in ['3', '2', '1', 'Go!']]
        self.win_time = time.time()
        while self.is_playing_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.pause_game(screen)
            pressed = pygame.key.get_pressed()
            current_time = time.time()
            if self.prob_of_new_meteor():
                self.add_meteor()
            self.overload_meteors()
            self.change_wind()
            self.change_acc(pressed, current_time)
            if self.game_started:
                self.add_gravity()
                self.add_wind()
            self.add_air_resistance()
            self.change_rocket_position()
            screen.fill(self.background_color)
            screen.blit(self.background.image, self.background.rect)
            pygame.draw.lines(screen, colors['white'], 0, [(i, self.surface[i]) for i in range(self.max_x)], 10)
            self.fill_surface(screen)
            self.draw_meteors(screen)
            self.show_speed(screen)
            self.draw_rocket(screen, current_time)
            self.set_game_status()
            if self.is_won:
                self.game_won(screen)
            elif self.is_lost:
                self.game_lost(screen)
            self.show_counting_down(counting_texts, screen, current_time)
            self.clock.tick(self.tick_time)
            pygame.display.flip()

    def show_counting_down(self, counting_texts: List[pygame.Surface], screen: pygame.Surface, current_time: float):
        """
        Method displays counting down at the beginning of every challenge!
        :param counting_texts: texts that should be displayed
        :param screen: Screen on which counting should be displayed
        :param current_time: current time
        """
        time_diff = current_time - self.win_time
        if time_diff <= self.count_down_time:
            text_num = int(1.8 * time_diff)
            self.show_text(screen, counting_texts[text_num], 1 / 2, 1 / 2)

    def game_lost(self, screen: pygame.Surface):
        """
        Method is responsible for handling lost game
        :param screen: main screen
        """
        if self.game_option[1]:
            s = pygame.mixer.Sound('death.wav')
            s.play()
        self.game_over(screen)

    def prob_of_new_meteor(self):
        """ Generates new meteors with probability depending on option set in option menu """
        probabilities = [0.01, 0.03, 0.06, 0.1]
        return r.random() < probabilities[self.game_option[0]]

    def draw_meteors(self, screen: pygame.Surface):
        """
        Method responsible for displaying meteors on the screen and for move of meteors
        :param screen: main screen
        """
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

    def overload_meteors(self):
        """
        If meteor is out of the sight it deletes it
        """
        for meteor in self.list_of_meteors:
            if not meteor.is_visible(self.max_x, self.max_y):
                self.list_of_meteors.remove(meteor)

    def add_meteor(self):
        """
        Add new meteor to the list if it is possible
        """
        if len(self.list_of_meteors) < self.maximum_number_of_meteors:
            brzeg = 100
            if r.random() < 0.7:
                y = -brzeg
                x = r.random() * self.max_x
                x_acc = r.random() * 3 - 1.5
                y_acc = r.random() * 2 + 1
            else:
                if r.random() < 0.5:
                    y = r.random() * self.max_y / 3
                    x = self.max_x + brzeg
                    x_acc = - r.random() * 3 - 1
                    y_acc = r.random() * 3 - 1
                else:
                    y = r.random() * self.max_y / 4
                    x = -brzeg
                    x_acc = r.random() * 3 + 1
                    y_acc = r.random() * 3 - 2.5
            rotation = 0
            rotation_speed = r.randint(1, 3)
            rotation_counter = 0
            size = r.choice([70, 60, 50, 40, 30])
            rotation_direction = r.choice([-1, 1])
            meteor = Meteor(x, y, x_acc, y_acc, rotation, rotation_counter, rotation_speed, rotation_direction, size)
            self.list_of_meteors.append(meteor)

    def set_game_status(self):
        """
        Method responsible for checking if game should end (because of win or lose) and setting appropriate flags
        """
        if not 0 < self.rocket.x < self.max_x - self.rocket.width:
            self.is_lost = True
        elif not 0 < self.rocket.y < self.max_y - self.rocket.height:
            self.is_lost = True
        for x, y in self.rocket.hit_box:
            if not y <= self.surface[x]:
                if abs(self.acc.x + self.acc.y) < 5 and \
                        self.landing_site[0][0] < self.rocket.x < self.landing_site[0][1]:
                    self.is_won = True
                    break
                self.is_lost = True
                break
        self.is_meteor_collided()

    def is_meteor_collided(self):
        """
        Check that is collision between rocket and any meteor
        """
        for meteor in self.list_of_meteors:
            for x, y in self.rocket.hit_box:
                if ((meteor.x + meteor.size) - x) ** 2 + ((meteor.y + meteor.size) - y) ** 2 <= 0.81 * meteor.size ** 2:
                    self.is_lost = True

    def change_rocket_position(self):
        """ Method enables changing position of a rocket if not pause and game started """
        if not self.pause and self.game_started:
            self.pos += self.acc

    def add_air_resistance(self):
        """ Adds air resistance to the rocket acceleration """
        if not self.pause:
            self.acc *= (1 - self.air_res / self.tick_time)

    def add_gravity(self):
        """ Adds gravity force to pull down the rocket """
        if not self.pause:
            self.acc.y += self.gravity / self.tick_time

    def add_wind(self):
        """ Adds wind force """
        self.acc.x -= self.wind

    def change_acc(self, pressed: List, current_time: float):
        """
        Method responsible for changing acceleration of a rocket depending on pressed keys. 
        :param pressed: pygame list with pressed keys
        :param current_time: current time flag preserves move before game starts
        """
        self.pause = False
        self.is_force = False
        if pressed[pygame.K_UP] and current_time - self.win_time > self.count_down_time:
            self.acc.y -= self.move
            self.is_force = True
            if not self.game_started:
                self.game_started = True
                self.acc.y -= 3
        if pressed[pygame.K_DOWN]:
            if self.acc.y < 0:
                self.acc.y = min(0, self.acc.y + self.move // 4)
        if pressed[pygame.K_LEFT]:
            if self.acc.y != 0:
                self.acc.x -= self.move / 2
        if pressed[pygame.K_RIGHT]:
            if self.acc.y != 0:
                self.acc.x += self.move / 2
        if pressed[pygame.K_SPACE]:
            self.pause = True

    def show_text(self, screen: pygame.Surface, text: pygame.Surface, x_ratio: float, y_ratio: float):
        """
        Method responsible for showing text on screen. 
        :param screen: main display
        :param text: text we want to show
        :param x_ratio: x / max_x, ratio where should middle of a text appear according to x axis
        :param y_ratio: y / max_y, ratio where should middle of a text appear according to y axis
        """
        x_pos = x_ratio * (self.max_x - text.get_width())
        y_pos = y_ratio * (self.max_y - text.get_height())
        screen.blit(text, (x_pos, y_pos))

    def game_over(self, screen: pygame.Surface):
        """
        Menu which will be shown after losing the game.
        :param screen: main display 
        """
        game_over_text = create_text("Game Over", self.font, 110, (255, 0, 0))
        continue_text = create_text("Press space to restart game", self.font, 35, (255, 0, 0))
        back_to_menu = create_text("Press escape to back to menu", self.font, 35, (255, 0, 0))

        self.show_text(screen, game_over_text, 1 / 2, 1 / 4)
        self.show_text(screen, continue_text, 1 / 2, 4 / 11)
        self.show_text(screen, back_to_menu, 1 / 2, 5 / 11)
        while self.is_lost:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_stage()
                    elif event.key == pygame.K_ESCAPE:
                        self.is_lost = False
                        self.is_playing_game = False
                        self.game_started = False
            self.clock.tick(self.tick_time)

    def reset_stage(self):
        """ Resets settings of current game """
        self.init_pos()
        self.reset_acc()
        self.reset_meteors()
        self.game_started = False
        self.is_lost = False
        self.is_won = False
        self.reset_wind()
        self.set_wind_on_start()
        self.win_time = time.time()

    def game_won(self, screen: pygame.Surface):
        """
        Planned behaviour after landing on landing site
        :param screen: main display 
        """
        if self.game_option[1]:
            s = pygame.mixer.Sound('victory.wav')
            s.play()
        self.cutscene()
        self.reset_stage()

    def draw_rocket(self, screen: pygame.Surface, current_time: float):
        """
        Method responsible for drawing rocket in the right position
        :param screen: main display
        :param current_time: preserves image change before game start
        """
        image = self.rocket.get_image(self.acc, self.is_force, (current_time - self.win_time) > 3)
        self.rocket.set_pos(self.pos.x, self.pos.y)
        self.rocket.set_width(image.get_width())
        self.rocket.set_height(image.get_height())
        screen.blit(image, self.rocket)
