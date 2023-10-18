def __create_adjacency_matrix(self):
        """!
        @brief Creates 2D adjacency matrix (list of lists) where each element described existence of link between points (means that points are neighbors).
        
        """
        
        size_data = len(self.__pointer_data);
        
        self.__adjacency_matrix = [ [ 0 for i in range(size_data) ] for j in range(size_data) ];
        for i in range(0, size_data):
            for j in range(i + 1, size_data):
                distance = euclidean_distance(self.__pointer_data[i], self.__pointer_data[j]);
                if (distance <= self.__eps):
                    self.__adjacency_matrix[i][j] = 1;
                    self.__adjacency_matrix[j][i] = 1;