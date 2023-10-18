def __get_neighbors(self, cell):
        """!
        @brief Returns neighbors for specified CLIQUE block as clique_block objects.

        @return (list) Neighbors as clique_block objects.

        """
        neighbors = []
        location_neighbors = cell.get_location_neighbors(self.__amount_intervals)

        for i in range(len(location_neighbors)):
            key = self.__location_to_key(location_neighbors[i])
            candidate_neighbor = self.__cell_map[key]

            if not candidate_neighbor.visited:
                candidate_neighbor.visited = True
                neighbors.append(candidate_neighbor)

        return neighbors