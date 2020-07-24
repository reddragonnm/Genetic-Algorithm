# This is the smart dots file!

import pygame as pg
import random


def random_path(length):
    path = [random.randint(0, 2) for _ in range(length)]
    return path


class Rocket:
    def __init__(self, fuel):
        self.genes = random_path(fuel)
        self.fitness = 0
        self.color = tuple([random.randint(0, 255) for _ in range(3)])
        self.end_pos = None
        self.fuel_used = None

    def crossover(self, other):
        child = Rocket(len(self.genes))
        midpoint = random.randint(0, len(self.genes))

        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = other.genes[i]

        return child

    def draw(self, screen, pos):
        if self.end_pos is None:
            circle = pg.draw.circle(screen, self.color, pos, 5)
            return circle
        else:
            circle = pg.draw.circle(screen, self.color, self.end_pos, 5)
            return circle

    def mutate(self, mutation_rate):
        for index in range(len(self.genes)):
            if random.random() <= mutation_rate:
                choices = [0, 1, 2]
                choices.remove(self.genes[index])
                choice = random.choice(choices)
                self.genes[index] = choice

    def calc_fitness(self, target):
        dist = ((self.end_pos[0] - target[0])**2 +
                (self.end_pos[1] - target[1])**2)**0.5
        multiplier = 10000

        try:
            self.fitness = 1 / dist
        except ZeroDivisionError:
            self.fitness = 1

        self.fitness = int(self.fitness * multiplier)
