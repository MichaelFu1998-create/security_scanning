def _create_connections(self, graph_matrix):
        """!
        @brief Creates connection in the network in line with graph.
        
        @param[in] graph_matrix (list): Matrix representation of the graph.
        
        """
        
        for row in range(0, len(graph_matrix)):
            for column in range (0, len(graph_matrix[row])):
                if (graph_matrix[row][column] > 0):
                    self.set_connection(row, column);