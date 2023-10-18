def collect_mean(self, fitness_functions):
        """!
        @brief Stores average value of fitness function among chromosomes on specific iteration.
        
        @param[in] fitness_functions (float): Average value of fitness functions among chromosomes.
        
        """

        if not self._need_mean_ff:
            return

        self._mean_ff_result.append(np.mean(fitness_functions))