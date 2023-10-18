def __create_weights_delaunay_triangulation(self, stimulus):
        """!
        @brief Create weight Denlauny triangulation structure between neurons in line with stimulus.
        
        @param[in] stimulus (list): External stimulus for the chaotic neural network.
        
        """
        
        points = numpy.array(stimulus)
        triangulation = Delaunay(points)
        
        for triangle in triangulation.simplices:
            for index_tri_point1 in range(len(triangle)):
                for index_tri_point2 in range(index_tri_point1 + 1, len(triangle)):
                    index_point1 = triangle[index_tri_point1]
                    index_point2 = triangle[index_tri_point2]
                    
                    weight = self.__calculate_weight(stimulus[index_point1], stimulus[index_point2])
                    
                    self.__weights[index_point1][index_point2] = weight
                    self.__weights[index_point2][index_point1] = weight
                    
                    self.__weights_summary[index_point1] += weight
                    self.__weights_summary[index_point2] += weight