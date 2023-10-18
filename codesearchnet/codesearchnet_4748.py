def _select(chromosomes, data, count_clusters, select_coeff):
        """!
        @brief Performs selection procedure where new chromosomes are calculated.
        
        @param[in] chromosomes (numpy.array): Chromosomes 
        
        """

        # Calc centers
        centres = ga_math.get_centres(chromosomes, data, count_clusters)

        # Calc fitness functions
        fitness = genetic_algorithm._calc_fitness_function(centres, data, chromosomes)

        for _idx in range(len(fitness)):
            fitness[_idx] = math.exp(1 + fitness[_idx] * select_coeff)

        # Calc probability vector
        probabilities = ga_math.calc_probability_vector(fitness)

        # Select P chromosomes with probabilities
        new_chromosomes = np.zeros(chromosomes.shape, dtype=np.int)

        # Selecting
        for _idx in range(len(chromosomes)):
            new_chromosomes[_idx] = chromosomes[ga_math.get_uniform(probabilities)]

        return new_chromosomes