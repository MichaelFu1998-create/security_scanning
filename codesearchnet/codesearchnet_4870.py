def __get_amount_color(self, node_indexes, color_number):
        """!
        @brief Countes how many nodes has color 'color_number'.
        
        @param[in] node_indexes (list): Indexes of graph nodes for checking.
        @param[in] color_number (uint): Number of color that is searched in nodes.
        
        @return (uint) Number found nodes with the specified color 'color_number'.
        
        """
        
        color_counter = 0;  
        for index in node_indexes:
            if (self.__coloring[index] == color_number):
                color_counter += 1;
        
        return color_counter;