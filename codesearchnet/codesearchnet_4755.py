def _calc_fitness_function(centres, data, chromosomes):
        """!
        @brief Calculate fitness function values for chromosomes.
        
        @param[in] centres (list): Cluster centers.
        @param[in] data (list): Input data that is used for clustering process.
        @param[in] chromosomes (list): Chromosomes whose fitness function's values are calculated.
        
        @return (list) Fitness function value for each chromosome correspondingly.
        
        """

        # Get count of chromosomes and clusters
        count_chromosome = len(chromosomes)

        # Initialize fitness function values
        fitness_function = np.zeros(count_chromosome)

        # Calc fitness function for each chromosome
        for _idx_chromosome in range(count_chromosome):

            # Get centers for a selected chromosome
            centres_data = np.zeros(data.shape)

            # Fill data centres
            for _idx in range(len(data)):
                centres_data[_idx] = centres[_idx_chromosome][chromosomes[_idx_chromosome][_idx]]

            # Get City Block distance for a chromosome
            fitness_function[_idx_chromosome] += np.sum(abs(data - centres_data))

        return fitness_function