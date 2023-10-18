def process(self):
        """!
        @brief Perform clustering procedure in line with rule of genetic clustering algorithm.
        
        @see get_clusters()
        
        """

        # Initialize population
        chromosomes = self._init_population(self._count_clusters, len(self._data), self._chromosome_count)

        # Initialize the Best solution
        best_chromosome, best_ff, first_fitness_functions \
            = self._get_best_chromosome(chromosomes, self._data, self._count_clusters)

        # Save best result into observer
        if self._observer is not None:
            self._observer.collect_global_best(best_chromosome, best_ff)
            self._observer.collect_population_best(best_chromosome, best_ff)
            self._observer.collect_mean(first_fitness_functions)

        # Next population
        for _ in range(self._population_count):

            # Select
            chromosomes = self._select(chromosomes, self._data, self._count_clusters, self._select_coeff)

            # Crossover
            self._crossover(chromosomes)

            # Mutation
            self._mutation(chromosomes, self._count_clusters, self._count_mutation_gens, self._coeff_mutation_count)

            # Update the Best Solution
            new_best_chromosome, new_best_ff, fitness_functions \
                = self._get_best_chromosome(chromosomes, self._data, self._count_clusters)

            # Get best chromosome
            if new_best_ff < best_ff:
                best_ff = new_best_ff
                best_chromosome = new_best_chromosome

            # Save best result into observer
            if self._observer is not None:
                self._observer.collect_global_best(best_chromosome, best_ff)
                self._observer.collect_population_best(new_best_chromosome, new_best_ff)
                self._observer.collect_mean(fitness_functions)

        # Save result
        self._result_clustering['best_chromosome'] = best_chromosome
        self._result_clustering['best_fitness_function'] = best_ff

        return best_chromosome, best_ff