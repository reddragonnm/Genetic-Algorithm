from population import Population

target = 300, 50
max_pop = 500
mutation_rate = 0.001
start_point = 300, 550
fuel = 100

done = False

population = Population(start_point, target, mutation_rate, max_pop, fuel)

while not done:
    population.calc_fitness()
    population.natural_selection()
    population.reproduce()

    done = population.finished
