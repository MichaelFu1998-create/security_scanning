def collect_global_best(self, best_chromosome, best_fitness_function):
        """!
        @brief Stores the best chromosome and its fitness function's value.
        
        @param[in] best_chromosome (list): The best chromosome that were observed.
        @param[in] best_fitness_function (float): Fitness function value of the best chromosome.
        
        """

        if not self._need_global_best:
            return

        self._global_best_result['chromosome'].append(best_chromosome)
        self._global_best_result['fitness_function'].append(best_fitness_function)