from dna import Qtable
from environment import GameEnv
import random

env = GameEnv()


class Population:
    def __init__(self, target_score, mutation_rate, max_pop):
        self.target = target_score
        self.mutation_rate = mutation_rate

        self.population = [Qtable() for _ in range(max_pop)]
        self.mating_pool = []
        self.finished = False
        self.generations = 1

    def calc_fitness(self):
        qtables = [member.qtable for member in self.population]

        env.birds_qtable_pool(qtables)
        env.simulate(self.target, self.generations)

        fitness_lst = env.return_fitness()

        for i in range(len(self.population)):
            self.population[i].calc_fitness(fitness_lst[i])

    def natural_selection(self):
        self.mating_pool = []

        for member in self.population:
            for _ in range(member.fitness):
                self.mating_pool.append(member)

    def reproduce(self):
        for n in range(len(self.population)):
            try:
                member1, member2 = random.sample(self.mating_pool, 2)
            except:
                member1, member2 = [Qtable() for _ in range(2)]

            child = member1.crossover(member2)
            child.mutate(self.mutation_rate)
            self.population[n] = child

        self.generations += 1
