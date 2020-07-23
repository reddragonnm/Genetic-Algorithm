from population import Population

target = 99999999999999
max_pop = 500
mutation_rate = 0.05

done = False

population = Population(target, mutation_rate, max_pop)

while not done:
    population.calc_fitness()
    population.natural_selection()
    population.reproduce()

    done = population.finished
