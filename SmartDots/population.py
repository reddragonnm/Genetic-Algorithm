import pygame as pg
from dna import Rocket
import random

pg.init()
pg.font.init()
font = pg.font.Font('freesansbold.ttf', 16)

FPS = 20
fpsClock = pg.time.Clock()

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
WHITE = 255, 255, 255


class Population:
    def __init__(self, start_point, target, mutation_rate, max_pop, fuel):
        self.target = target
        self.mutation_rate = mutation_rate
        self.fuel = fuel
        self.start_point = start_point

        self.screen_dim = 600, 600
        self.screen = pg.display.set_mode(self.screen_dim)

        self.population = [Rocket(fuel) for _ in range(max_pop)]
        self.mating_pool = []
        self.finished = False
        self.reached_target = 0

        self.obstacles = [
            (0, 0, 5, self.screen_dim[1]),
            (0, 0, self.screen_dim[0], 5),
            (0, self.screen_dim[1] - 5, self.screen_dim[0], 5),
            (self.screen_dim[0] - 5, 0, 5, self.screen_dim[1]),
            (100, 200, 400, 50)
        ]

        # (100, 200, 400, 50)

        self.generations = 0
        self.max_dots = 0

    def pos_list_from_genes(self, lst):
        pos_list_final = []

        for genes in lst:
            pos_list = [self.start_point]
            angle = 0
            x, y = self.start_point

            for turn in genes:
                if turn == 0:
                    angle -= 45
                elif turn == 2:
                    angle += 45

                if angle > 360:
                    angle -= 360
                elif angle < 0:
                    angle += 360

                if 270 < angle or angle < 90:
                    y -= 10
                elif 90 < angle < 270:
                    y += 10

                if 0 < angle < 180:
                    x += 10
                elif angle > 180:
                    x -= 10

                pos_list.append((x, y))

            pos_list_final.append(pos_list)

        return pos_list_final

    def calc_fitness(self):
        global FPS
        pos_list = self.pos_list_from_genes(
            [member.genes for member in self.population])
        self.reached_target = 0

        pg.font.init()
        font = pg.font.Font('freesansbold.ttf', 16)

        for cycle in range(self.fuel):
            self.screen.fill(WHITE)

            target = pg.draw.circle(self.screen, (BLUE), self.target, 15)
            obs_objects = [pg.draw.rect(self.screen, (GREEN), obs)
                           for obs in self.obstacles]

            for n, pos in enumerate(pos_list):
                circle = self.population[n].draw(self.screen, pos[cycle])

                for obs in obs_objects:
                    if circle.colliderect(obs):
                        self.population[n].end_pos = pos[cycle - 1]
                        self.population[n].fuel_used = cycle
                        break

                if circle.colliderect(target):
                    if self.population[n].end_pos is None:
                        self.reached_target += 1

                    self.population[n].end_pos = self.target
                    self.population[n].fuel_used = cycle

            if self.reached_target > self.max_dots:
                self.max_dots = self.reached_target

            self.screen.blit(font.render(
                f"Generation: {self.generations}", True, RED), (20, 450))
            self.screen.blit(font.render(
                f"Fuel left: {self.fuel - cycle}", True, RED), (20, 500))
            self.screen.blit(font.render(
                f"Dots reached target : {self.reached_target}", True, RED), (20, 550))
            self.screen.blit(font.render(
                f"Max dots : {self.max_dots}", True, RED), (20, 400))

            pg.display.update()
            fpsClock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        FPS += 5
                    elif event.key == pg.K_s:
                        FPS -= 5

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.target = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    del font
                    pg.quit()
                    pg.font.quit()
                    quit()

        for n, member in enumerate(self.population):
            if member.end_pos is None:
                member.end_pos = pos_list[n][-1]

            if member.fuel_used is None:
                member.fuel_used = self.fuel

            member.calc_fitness(self.target)

    def natural_selection(self):
        self.mating_pool = []

        for member in self.population:
            for _ in range(member.fitness):
                self.mating_pool.append(member)

    def reproduce(self):
        # if self.max_dots > 0:
        #     self.mutation_rate *= 0.8

        for n in range(len(self.population)):
            try:
                member1, member2 = random.sample(self.mating_pool, 2)
            except Exception as e:
                member1, member2 = [Rocket(self.fuel) for _ in range(2)]

            child = member1.crossover(member2)
            child.mutate(self.mutation_rate)
            self.population[n] = child

        self.generations += 1


del font
pg.quit()
