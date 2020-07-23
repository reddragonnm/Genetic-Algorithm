from population import Population

target = "To be or not to be."
max_pop = 500
mutation_rate = 0.01
done = False

population = Population(target, mutation_rate, max_pop)

while not done:
    population.natural_selection()
    population.generate()
    population.calc_fitness()
    population.evaluate()

    done = population.finished
    print(population.best, population.generations, population.avg_fitness())
