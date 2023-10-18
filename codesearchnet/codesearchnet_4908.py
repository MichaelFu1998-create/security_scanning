def __find_pair_clusters(self, clusters):
        """!
        @brief Returns pair of clusters that are best candidates for merging in line with goodness measure.
               The pair of clusters for which the above goodness measure is maximum is the best pair of clusters to be merged.
               
        @param[in] clusters (list): List of clusters that have been allocated during processing, each cluster is represented by list of indexes of points from the input data set.
        
        @return (list) List that contains two indexes of clusters (from list 'clusters') that should be merged on this step.
                It can be equals to [-1, -1] when no links between clusters.
        
        """
        
        maximum_goodness = 0.0;
        cluster_indexes = [-1, -1];
        
        for i in range(0, len(clusters)):
            for j in range(i + 1, len(clusters)):
                goodness = self.__calculate_goodness(clusters[i], clusters[j]);
                if (goodness > maximum_goodness):
                    maximum_goodness = goodness;
                    cluster_indexes = [i, j];
        
        return cluster_indexes;