import random


def random_qtable():
    qtable = {}
    for i in range(-600, 600):
        qtable[i] = random.choice([0, 1])

    return qtable


class Qtable:
    def __init__(self):
        self.fitness = 0
        self.qtable = random_qtable()

    def mutate(self, mutation_rate):
        for key in self.qtable:
            if random.random() <= mutation_rate:
                choices = [0, 1]
                choices.remove(self.qtable[key])
                self.qtable[key] = random.choice(choices)

    def crossover(self, other):
        child = Qtable()
        midpoint = random.randint(0, len(self.qtable))

        for i, key in enumerate(self.qtable):
            if i > midpoint:
                child.qtable[key] = self.qtable[key]
            else:
                child.qtable[key] = other.qtable[key]

        return child

    def calc_fitness(self, distance_travelled):
        self.fitness = distance_travelled
