def __calculate_neighborhood(self, block_max_corner):
        """!
        @brief Calculates neighborhood score that defined whether blocks are neighbors.

        @param[in] block_max_corner (list): Maximum coordinates of other block.

        @return (uint) Neighborhood score.

        """
        dimension = len(block_max_corner)

        length_edges = [self.__max_corner[i] - self.__min_corner[i] for i in range(dimension)]

        neighborhood_score = 0
        for i in range(dimension):
            diff = abs(block_max_corner[i] - self.__max_corner[i])

            if diff <= length_edges[i] + length_edges[i] * 0.0001:
                neighborhood_score += 1

        return neighborhood_score