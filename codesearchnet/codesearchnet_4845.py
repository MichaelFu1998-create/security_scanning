def __expand_cluster(self, cell):
        """!
        @brief Tries to expand cluster from specified cell.
        @details During expanding points are marked as noise or append to new cluster.

        @param[in] cell (clique_block): CLIQUE block from that cluster should be expanded.

        """
        cell.visited = True

        if len(cell.points) <= self.__density_threshold:
            if len(cell.points) > 0:
                self.__noise.extend(cell.points)

            return

        cluster = cell.points[:]
        neighbors = self.__get_neighbors(cell)

        for neighbor in neighbors:
            if len(neighbor.points) > self.__density_threshold:
                cluster.extend(neighbor.points)
                neighbors += self.__get_neighbors(neighbor)

            elif len(neighbor.points) > 0:
                self.__noise.extend(neighbor.points)

        self.__clusters.append(cluster)