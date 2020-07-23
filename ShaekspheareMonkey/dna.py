import random

class DNA:
    def __init__(self, length):
        self.genes = self.random_str(length)
        self.fitness = 0

    def get_phrase(self):
        return "".join(self.genes)

    def calc_fitness(self, target):
        for n , letter in enumerate(target):
            if letter == self.genes[n]:
                self.fitness += 1

    def crossover(self, other):
        child = DNA(len(self.genes))
        midpoint = random.randint(0, len(self.genes))

        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = other.genes[i]

        return child

    def mutate(self, mutation_rate):
        for index in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[index] = self.random_str()

    @staticmethod
    def random_str(length=1):
        alphabets = " qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.'!"
        if length == 1:
            return random.choice(alphabets)
        return random.sample(alphabets, length)
