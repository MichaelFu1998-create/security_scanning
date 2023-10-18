def __generate_point(self, index_cluster):
        """!
        @brief Generates point in line with parameters of specified cluster.

        @param[in] index_cluster (uint): Index of cluster whose parameters are used for point generation.

        @return (list) New generated point in line with normal distribution and cluster parameters.

        """
        return [ random.gauss(self.__cluster_centers[index_cluster][index_dimension],
                              self.__cluster_width[index_cluster] / 2.0)
                 for index_dimension in range(self.__dimension) ]