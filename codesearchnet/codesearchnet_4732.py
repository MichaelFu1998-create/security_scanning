def __generate_cluster_centers(self, width):
        """!
        @brief Generates centers (means in statistical term) for clusters.

        @param[in] width (list): Width of generated clusters.

        @return (list) Generated centers in line with normal distribution.

        """
        centers = []
        default_offset = max(width) * 4.0
        for i in range(self.__amount_clusters):
            center = [ random.gauss(i * default_offset, width[i] / 2.0) for _ in range(self.__dimension) ]
            centers.append(center)

        return centers