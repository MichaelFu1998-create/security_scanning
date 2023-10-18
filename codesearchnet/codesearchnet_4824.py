def allocate_clusters(self, eps = 0.01, indexes = None, iteration = None):
        """!
        @brief Returns list of clusters in line with state of ocillators (phases).
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one cluster.
        @param[in] indexes (list): List of real object indexes and it should be equal to amount of oscillators (in case of 'None' - indexes are in range [0; amount_oscillators]).
        @param[in] iteration (uint): Iteration of simulation that should be used for allocation.
        
        @return (list) List of clusters, for example [ [cluster1], [cluster2], ... ].)
        
        """
        
        return self.allocate_sync_ensembles(eps, indexes, iteration);