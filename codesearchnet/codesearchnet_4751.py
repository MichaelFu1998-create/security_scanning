def _crossover_a_pair(chromosome_1, chromosome_2, mask):
        """!
        @brief Crossovers a pair of chromosomes.
        
        @param[in] chromosome_1 (numpy.array): The first chromosome for crossover.
        @param[in] chromosome_2 (numpy.array): The second chromosome for crossover.
        @param[in] mask (numpy.array): Crossover mask that defines which genes should be swapped.
        
        """

        for _idx in range(len(chromosome_1)):

            if mask[_idx] == 1:
                # Swap values
                chromosome_1[_idx], chromosome_2[_idx] = chromosome_2[_idx], chromosome_1[_idx]