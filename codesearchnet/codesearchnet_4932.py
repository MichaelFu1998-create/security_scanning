def __update_clusters(self):
        """!
        @brief Calculate distance (in line with specified metric) to each point from the each cluster. Nearest points
                are captured by according clusters and as a result clusters are updated.
        
        @return (list) Updated clusters as list of clusters. Each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for _ in range(len(self.__centers))]
        
        dataset_differences = self.__calculate_dataset_difference(len(clusters))
        
        optimum_indexes = numpy.argmin(dataset_differences, axis=0)
        for index_point in range(len(optimum_indexes)):
            index_cluster = optimum_indexes[index_point]
            clusters[index_cluster].append(index_point)
        
        clusters = [cluster for cluster in clusters if len(cluster) > 0]

        return clusters