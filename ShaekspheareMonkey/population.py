from dna import DNA
import random

class Population:
    def __init__(self, target, mutation_rate, max_pop):
        self.target = target
        self.mutation_rate = mutation_rate

        self.population = [DNA(len(target)) for _ in range(max_pop)]
        self.mating_pool = []
        self.finished = False
        self.perfect_score = len(target)

        self.generations = 0
        self.best = ""
        self.max_fitness = 0

        self.calc_fitness()

    def calc_fitness(self):
        for member in self.population:
            member.calc_fitness(self.target)

    def natural_selection(self):
        self.mating_pool = []

        for member in self.population:
            if member.fitness > self.max_fitness:
                self.max_fitness = member.fitness

        for member in self.population:
            for _ in range(member.fitness):
                self.mating_pool.append(member)

    def generate(self):
        for n in range(len(self.population)):
            try:
                member1, member2 = random.sample(self.mating_pool, 2)
            except:
                member1, member2 = [DNA(len(self.target)) for _ in range(2)]

            child = member1.crossover(member2)
            child.mutate(self.mutation_rate)
            self.population[n] = child

        self.generations += 1

    def evaluate(self):
        world_record = 0
        index = 0

        for n, member in enumerate(self.population):
            if member.fitness > world_record:
                index = n
                world_record = member.fitness

        self.best = self.population[index].get_phrase()

        if world_record >= self.perfect_score:
            self.finished = True

    def avg_fitness(self):
        total = 0
        for member in self.population:
            total += member.fitness

        return total / len(self.population)

    def all_phrases(self):
        limit = min(len(self.population), 50)
        return "\n".join(self.population[0:limit])
