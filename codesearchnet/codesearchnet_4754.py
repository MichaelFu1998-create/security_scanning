def _get_best_chromosome(chromosomes, data, count_clusters):
        """!
        @brief Returns the current best chromosome.
        
        @param[in] chromosomes (list): Chromosomes that are used for searching.
        @param[in] data (list): Input data that is used for clustering process.
        @param[in] count_clusters (uint): Amount of clusters that should be allocated.
        
        @return (list, float, list) The best chromosome, its fitness function value and fitness function values for
                 all chromosomes.
        
        """

        # Calc centers
        centres = ga_math.get_centres(chromosomes, data, count_clusters)

        # Calc Fitness functions
        fitness_functions = genetic_algorithm._calc_fitness_function(centres, data, chromosomes)

        # Index of the best chromosome
        best_chromosome_idx = fitness_functions.argmin()

        # Get chromosome with the best fitness function
        return chromosomes[best_chromosome_idx], fitness_functions[best_chromosome_idx], fitness_functions