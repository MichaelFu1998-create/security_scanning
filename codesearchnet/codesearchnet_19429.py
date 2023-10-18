def genetic_algorithm(population, fitness_fn, ngen=1000, pmut=0.1):
    "[Fig. 4.8]"
    for i in range(ngen):
        new_population = []
        for i in len(population):
            fitnesses = map(fitness_fn, population)
            p1, p2 = weighted_sample_with_replacement(population, fitnesses, 2)
            child = p1.mate(p2)
            if random.uniform(0, 1) < pmut:
                child.mutate()
            new_population.append(child)
        population = new_population
    return argmax(population, fitness_fn)