def generate(self):
        """!
        @brief Generates data in line with generator parameters.

        """
        data_points = []

        for index_cluster in range(self.__amount_clusters):
            for _ in range(self.__cluster_sizes[index_cluster]):
                point = self.__generate_point(index_cluster)
                data_points.append(point)

        return data_points