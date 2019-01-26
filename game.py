# -*- coding: utf-8 -*-
"""
Module provides game itself
You can download needed sprites from here: https://www.mediafire.com/file/cb365fxtu8ivt2u/sprites.7z/file
"""
import math
import numpy
import os

import random as r

import pygame
from pygame.math import Vector2

from rocket import load_sprites

x = 500
y = 40
black = (255, 255, 255)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


def make_font(fonts, size):
    available = pygame.font.get_fonts()
    choices = map(lambda font: font.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}


def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font_preferences, size)
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


font_preferences = ["Papyrus", "Comic Sans MS"]


class Game:
    def __init__(self, size, rocket, sprites):
        self.chooses = [0, 0, 0] # wybory w opcjach, ale uwaga, to lista list
        self.sprites = sprites
        self.sprites_len = len(sprites[0])
        self.image = sprites[0][self.sprites_len // 2]
        self.max_x, self.max_y = size
        self.gravity = 10
        self.air_res = 0.8
        self.pos = None
        self.acc = None
        self.rocket = rocket
        self.clock = pygame.time.Clock()
        self.done = False
        self.not_lost_game = False
        self.won_game = False
        self.move = 0.5
        self.tick_time = 60
        self.pause = False
        self.is_force = False

    def init_pos(self):
        self.pos = Vector2(self.max_x / 2, self.max_y / 4)

    def reset_acc(self):
        self.acc = Vector2(0, 0)

    def main_menu(self, screen):
        not_chosen = True
        texts = ['Start game', 'Options', 'About', 'Exit']
        text_len = len(texts)
        option = 0
        while not_chosen:
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
                            not_chosen = False
                            self.done = True
                    elif event.key == pygame.K_ESCAPE:
                        self.done = True
                        not_chosen = False
                elif event.type == pygame.QUIT:
                    self.done = True
                    not_chosen = False

            screen.fill(black)
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

    def about(self, screen):
        is_about = True
        texts = ['Authors:', 'Kornel Raczak', 'Pawel Gorecki', 'Lukasz Polakiewicz', 'Press ESC']
        text_len = len(texts)
        while is_about:
            self.clock.tick(self.tick_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                        is_about = False

            screen.fill(black)
            colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 125, 125), (125, 125, 0)]
            for i, text in enumerate(texts):
                font_size = 60
                new_text = create_text(text, font_preferences, font_size, colors[i])
                x_pos = (self.max_x - new_text.get_width()) // 2
                y_pos = (1 + i) * (self.max_y - new_text.get_height()) // (2 + text_len) + font_size
                screen.blit(new_text, (x_pos, y_pos))
            pygame.display.flip()

    def option_menu(self,screen):
        not_chosen = True
        option_meteors = ["Meteors: easy", "Meteors: medium", "Meteors: hard", "Meteors: impossible"]
        options1 = ['Music: Off', 'Music: On']
        options2 = ['xD','dddd']
        options = [option_meteors, options1, options2]
        self.chooses_len = []
        for option in options:
            self.chooses_len.append(len(option))
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
                        self.chooses[option] = (self.chooses[option] - 1) % self.chooses_len[option]
                    elif event.key == pygame.K_RIGHT:
                       self. chooses[option] = (self.chooses[option] + 1) % self.chooses_len[option]
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if option == 0:
                            self.play_game(screen)
                        elif option == 1:
                            self.option_menu(screen)
                        elif option == 2:
                            self.about(screen)
                        elif option == 3:
                            not_chosen = False
                            self.done = True
                    elif event.key == pygame.K_ESCAPE:
                        self.done = True
                        not_chosen = False
                elif event.type == pygame.QUIT:
                    self.done = True
                    not_chosen = False

            screen.fill(black)
            color = (0, 0, 255)#, (255, 0, 0), (0, 255, 0), (0, 125, 125), (125, 125, 0)]
            for i, opt in enumerate(options):
                color = (0, 0, 255)
                font_size = 60
                what_to_write = opt[self.chooses[i]]
                if i == option:
                    #what_to_write = "-> " + what_to_write
                    color = (0,255,0)
                new_text = create_text(what_to_write, font_preferences, font_size, color)
                x_pos = (self.max_x - new_text.get_width()) // 2
                y_pos = (1 + i) * (self.max_y - new_text.get_height()) // (2 + text_len) + font_size
                screen.blit(new_text, (x_pos, y_pos))
            pygame.display.flip()

    def show_speed(self, screen):
        speed_x_val = abs(round(self.acc.x  / (2 / 173)))
        speed_y_val = abs(round(self.acc.y  / (2 / 173)))
        speed_x = create_text('Horizontal:  {} km/h'.format(speed_x_val), font_preferences, 20, (255, 0, 0))
        speed_y = create_text('Vertical:  {} km/h'.format(speed_y_val), font_preferences, 20, (255, 0, 0))
        screen.blit(speed_x, (10, 30))
        screen.blit(speed_y, (10, 10))
        
    def generate_surface(self, n, surface_length, rng):
        height = 1000
        width = 1400
        surf = []
        landing_site = [numpy.random.randint(surface_length,n-surface_length), height - numpy.random.randint(0, rng)]
        self.landing_site = [(landing_site[0]-surface_length)*width//n, (landing_site[0]+surface_length)*width//n]
        for i in range(n):
            if abs(i-landing_site[0])<=surface_length:
                surf.append([i*width//n, landing_site[1]])
            else:
                surf.append((i*width//n, height - numpy.random.randint(0, rng)))
        surf.append((width-1,height))
        self.surface = [0] * width
        print(self.landing_site)
        for i in range(n):
            for j in range(width//n):
                self.surface[i*width//n+j] = (surf[i][1] * (width//n-j) + surf[i+1][1] * j)//(width//n)
        return surf

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.max_x, self.max_y))
        self.main_menu(screen)

    def reset_meteors(self):
        self.list_of_meteors = []

    def play_game(self, screen):
        self.done = False
        self.init_pos()
        self.reset_acc()
        self.reset_meteors()
        planet_surface = self.generate_surface(100,5,500)
        #pygame.mixer.music.play()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pressed = pygame.key.get_pressed()
            if self.prob_of_new_meteor():
                self.add_meteor()
            self.change_acc(pressed)
            self.add_gravity()
            self.add_air_resistance()
            self.change_rocket_position()
            screen.fill(black)
            pygame.draw.lines(screen, 0, 0, planet_surface, 10)
            self.draw_meteors(screen)
            self.draw_rocket(screen)
            self.show_speed(screen)
            self.is_game_lost()
            pygame.display.flip()
            self.clock.tick(self.tick_time)
            if self.not_lost_game:
                if self.chooses[1]:
                    s = pygame.mixer.Sound('death.wav')
                    s.play()
                self.game_over(screen)
                self.list_of_meteors = []
            if self.won_game:
                if self.chooses[1]:
                    s = pygame.mixer.Sound('victory.wav')
                    s.play()
                self.game_won(screen)
                self.list_of_meteors = []

    def prob_of_new_meteor(self):
        liczniki = [0.01, 0.05, 0.1, 0.3]
        return r.random() < liczniki[self.chooses[0]]

    def draw_meteors(self, screen):
        self.image = self.sprites[-1]
        for i, [x, y, x_acc, y_acc] in enumerate(self.list_of_meteors):
            self.list_of_meteors[i][0] += x_acc
            self.list_of_meteors[i][1] += y_acc
            #print(x,' ',y)
            self.meteor = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
            pygame.draw.rect(screen, black, self.meteor)
            screen.blit(self.image, self.meteor)

    def add_meteor(self):
        mid_or_feed = r.random() < 0.8 #czy meteor leci z gory
        if(mid_or_feed):
            y = 0
            x = r.random() * self.max_x
            x_acc = r.random() * 2 - 4
            y_acc = r.random() * 2 + 1
        else:
            #czy z lewej czy z prawej strony
            if r.random() < 0.5: # z prawej
                y = r.random() * self.max_y / 3  # na wysokosci 1/3
                x = self.max_y  # z lewej albo z prawej
                x_acc = - r.random() * 2
                y_acc = r.random() * 2 - 1
            else:
                y = r.random() * self.max_y / 3  # na wysokosci 1/3
                x = 0  # z lewej albo z prawej
                x_acc = r.random() * 2
                y_acc = r.random() * 2 - 1
        meteor = [x, y, x_acc, y_acc]
        self.list_of_meteors.append(meteor)

    def is_game_lost(self):
        if not 0 < self.rocket.x < self.max_x - self.rocket.width:
            self.not_lost_game = True
        if not 0 < self.rocket.y < self.max_y - self.rocket.height:
            self.not_lost_game = True
        if not self.rocket.y <= self.surface[self.rocket.x] - self.rocket.height:
            if abs(self.acc.x)<2 and abs(self.acc.y)<5 and self.landing_site[0] < self.rocket.x < self.landing_site[1]:
                self.won_game = True
            else:
                self.not_lost_game = True
        for i in self.list_of_meteors:
            for j in self.hitbox:
                radius = 70
                if ((i[0]+radius) - j[0]) ** 2 + ((i[1]+radius) - j[1]) **2 <= radius ** 2:
                    self.not_lost_game = True

    def meteorits_collision(self):
        pass

    def draw_rocket(self, screen):
        n = 24
        sprite_num = int(round(self.acc.x * n / self.sprites_len)) + self.sprites_len // 2
        if sprite_num >= self.sprites_len - 1:
            sprite_num = self.sprites_len - 1
        elif sprite_num < 0:
            sprite_num = 0
        self.image = self.sprites[self.is_force][sprite_num]
        self.rocket = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())
        self.hitbox = [(self.rocket.x + self.rocket.width//2 + math.cos((90-sprite_num + i*45)*math.pi/180) * 15, 
                        self.rocket.y + self.rocket.height//2 + math.sin((90-sprite_num + i*45)*math.pi/180) * 35)
                       for i in range(8)]
        pygame.draw.rect(screen, black, self.rocket)
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
        while self.not_lost_game:
            game_over_text = create_text("Game Over", font_preferences, 110, (255, 0, 0))
            continue_text = create_text("Press space to restart game", font_preferences, 35, (255, 0, 0))
            back_to_menu = create_text("Press escape to back to menu", font_preferences, 35, (255, 0, 0))

            self.show_text(screen, game_over_text, 1 / 2, 1 / 4)
            self.show_text(screen, continue_text, 1 / 2, 4 / 11)
            self.show_text(screen, back_to_menu, 1 / 2, 5 / 11)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.not_lost_game = False
                        self.init_pos()
                        self.reset_acc()
                    elif event.key == pygame.K_ESCAPE:
                        self.not_lost_game = False
                        self.done = True
            self.clock.tick(self.tick_time)
    
    def game_won(self, screen):
        '''higher productivity = higher LOC'''
        while self.won_game:
            game_over_text = create_text("You won!", font_preferences, 110, (128, 128, 0))
            continue_text = create_text("Press space to restart game", font_preferences, 35, (128, 128, 0))
            back_to_menu = create_text("Press escape to back to menu", font_preferences, 35, (128, 128, 0))

            self.show_text(screen, game_over_text, 1 / 2, 1 / 4)
            self.show_text(screen, continue_text, 1 / 2, 4 / 11)
            self.show_text(screen, back_to_menu, 1 / 2, 5 / 11)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.won_game = False
                        self.init_pos()
                        self.reset_acc()
                    elif event.key == pygame.K_ESCAPE:
                        self.won_game = False
                        self.done = True
            self.clock.tick(self.tick_time)


if __name__ == '__main__':
    size = (1400, 1000)
    rocket = pygame.Rect(size[0] / 2, size[1] / 2, 60, 60)
    sprites_no_acc = load_sprites(r'no_acc')
    sprites_acc = load_sprites(r'acc')
    meteor = pygame.image.load(r'meteors\meteor2.png')
    sprites = [sprites_no_acc, sprites_acc, meteor]
    game = Game(size, rocket, sprites)
    game.run()
    pygame.quit()
