import numpy as np
import time
import pygame as pg
import random

pg.init()
FPS = 10000  # frames per second setting
fpsClock = pg.time.Clock()
font = pg.font.Font('freesansbold.ttf', 32)

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
WHITE = 255, 255, 255


class Bird:
    def __init__(self, qtable):
        self.qtable = qtable
        self.distance_travelled = 0

        self.x = 150
        self.y = 300

        self.dead = False
        self.difference = 0

        self.bird = pg.image.load("Images\\bird.gif")
        self.bird_rect = None

    def perform_action(self, pipet_bottom_y, screen):
        if self.dead:
            return

        action = self.qtable[pipet_bottom_y - self.y]
        self.distance_travelled += 1

        if action == 1:
            self.jump()
        elif action == 0:
            self.fall()

        self.bird_rect = screen.blit(self.bird, (self.x, self.y))

    def check_collision(self, pipet_rect, pipeb_rect, ground_rect, pipet_bottom_y, gap):
        if self.bird_rect.colliderect(pipet_rect) or self.bird_rect.colliderect(pipeb_rect) or self.bird_rect.colliderect(ground_rect):
            self.dead = True
            self.difference = abs((pipet_bottom_y + gap // 2) - self.x)

    def check_removal(self, removal_list):
        if self.dead:
            removal_list.append(self)

        return removal_list

    def jump(self):
        if self.y > 0:
            self.y -= 30

    def fall(self):
        self.y += 10


class GameEnv:
    def __init__(self):
        self.generation = 0

        self.screen_dim = 400, 600
        self.screen = pg.display.set_mode(self.screen_dim)
        self.score = 0

        self.background = pg.transform.scale(pg.image.load("Images\\background.gif"),
                                             (self.screen_dim[0], self.screen_dim[1] - 100))

        self.ground = pg.image.load("Images\\ground.gif")
        self.pipet = pg.image.load("Images\\pipet.gif")
        self.pipeb = pg.image.load("Images\\pipeb.gif")

        self.bird_x, self.bird_y = 150, 300
        self.gap = 150
        self.score = 0
        self.max_score = 0

        self.bird_pl = None
        self.gn = None
        self.pt = None
        self.pb = None

        y = random.randint(0, self.screen_dim[1] - self.gap - 100)
        self.pipet_bottom_y, self.pipet_bottom_x = y, self.screen_dim[0]
        self.pipeb_top_y, self.pipeb_top_x = y + self.gap, self.screen_dim[0]

        self.birds = []
        self.permanent_bird_list = []

    def birds_qtable_pool(self, qtables):
        self.birds = []
        self.permanent_bird_list = []

        for qtable in qtables:
            bird = Bird(qtable)
            self.birds.append(bird)
            self.permanent_bird_list.append(bird)

    def simulate(self, target, generation):
        global FPS

        while True:
            self.move_background()
            self.move_pipes()

            removal_list = []

            for bird in self.birds:
                bird.perform_action(self.pipet_bottom_y, self.screen)

                bird.check_collision(
                    self.pt, self.pb, self.gn, self.pipet_bottom_y, self.gap)
                self.removal_list = bird.check_removal(removal_list)

                if bird.distance_travelled >= target:
                    self.removal_list.append(bird)

            for removal in removal_list:
                self.birds.remove(removal)

            self.screen.blit(font.render(
                f"Generation: {generation}", True, RED), (20, 450))

            self.screen.blit(font.render(
                f"Score: {self.score}", True, RED), (20, 400))

            self.screen.blit(font.render(
                f"Max Score: {self.max_score}", True, RED), (20, 350))

            pg.display.update()
            fpsClock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        FPS += 5
                    elif event.key == pg.K_s:
                        FPS -= 5

            if self.birds == []:
                break

        self.pipet_bottom_x = self.screen_dim[0]
        self.pipeb_top_x = self.screen_dim[0]

        if self.score > self.max_score:
            self.max_score = self.score

        self.score = 0

    def move_pipes(self):
        self.pipet_bottom_x -= 5
        self.pipeb_top_x -= 5

        if self.pipet_bottom_x <= 0:
            y = random.randint(0, self.screen_dim[1] - self.gap - 100)
            self.pipet_bottom_y, self.pipet_bottom_x = y, self.screen_dim[0]
            self.pipeb_top_y, self.pipeb_top_x = y + \
                self.gap, self.screen_dim[0]

            self.score += 1

    def move_background(self):
        self.screen.blit(self.background, (0, 0))
        self.pt = self.screen.blit(self.pipet, (self.pipet_bottom_x,
                                                self.pipet_bottom_y - self.pipet.get_height()))
        self.pb = self.screen.blit(
            self.pipeb, (self.pipeb_top_x, self.pipeb_top_y))
        self.gn = self.screen.blit(
            self.ground, (0, self.screen_dim[1] - 100))

    def reset(self):
        self.pipet_bottom_x = self.screen_dim[0]
        self.pipeb_top_x = self.screen_dim[0]

    def return_fitness(self):
        fitness_lst = []
        for bird in self.permanent_bird_list:
            fitness_lst.append(bird.distance_travelled + bird.difference)

        return fitness_lst
