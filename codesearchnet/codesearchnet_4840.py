def get_location_neighbors(self, edge):
        """!
        @brief Forms list of logical location of each neighbor for this particular CLIQUE block.

        @param[in] edge (uint): Amount of intervals in each dimension that is used for clustering process.

        @return (list) Logical location of each neighbor for this particular CLIQUE block.

        """
        neighbors = []

        for index_dimension in range(len(self.__logical_location)):
            if self.__logical_location[index_dimension] + 1 < edge:
                position = self.__logical_location[:]
                position[index_dimension] += 1
                neighbors.append(position)

            if self.__logical_location[index_dimension] - 1 >= 0:
                position = self.__logical_location[:]
                position[index_dimension] -= 1
                neighbors.append(position)

        return neighbors