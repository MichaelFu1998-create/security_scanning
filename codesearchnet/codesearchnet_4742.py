def collect_population_best(self, best_chromosome, best_fitness_function):
        """!
        @brief Stores the best chromosome for current specific iteration and its fitness function's value.
        
        @param[in] best_chromosome (list): The best chromosome on specific iteration.
        @param[in] best_fitness_function (float): Fitness function value of the chromosome.
        
        """

        if not self._need_population_best:
            return

        self._best_population_result['chromosome'].append(best_chromosome)
        self._best_population_result['fitness_function'].append(best_fitness_function)