def __expand_cluster(self, index_point):
        """!
        @brief Expands cluster from specified point in the input data space.
        
        @param[in] index_point (list): Index of a point from the data.

        @return (list) Return tuple of list of indexes that belong to the same cluster and list of points that are marked as noise: (cluster, noise), or None if nothing has been expanded.
        
        """
        
        cluster = None
        self.__visited[index_point] = True
        neighbors = self.__neighbor_searcher(index_point)
         
        if len(neighbors) >= self.__neighbors:
            cluster = [index_point]
             
            self.__belong[index_point] = True
             
            for i in neighbors:
                if self.__visited[i] is False:
                    self.__visited[i] = True

                    next_neighbors = self.__neighbor_searcher(i)
                     
                    if len(next_neighbors) >= self.__neighbors:
                        neighbors += [k for k in next_neighbors if ( (k in neighbors) == False) and k != index_point]
                 
                if self.__belong[i] is False:
                    cluster.append(i)
                    self.__belong[i] = True

        return cluster