def _init_population(count_clusters, count_data, chromosome_count):
        """!
        @brief Returns first population as a uniform random choice.
        
        @param[in] count_clusters (uint): Amount of clusters that should be allocated.
        @param[in] count_data (uint): Data size that is used for clustering process.
        @param[in] chromosome_count (uint):Amount of chromosome that is used for clustering.
        
        """

        population = np.random.randint(count_clusters, size=(chromosome_count, count_data))

        return population