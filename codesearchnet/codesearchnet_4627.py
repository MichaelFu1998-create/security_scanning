def find_node(self, point, cur_node = None):
        """!
        @brief Find node with coordinates that are defined by specified point.
        @details If node with specified parameters does not exist then None will be returned, 
                  otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node if it satisfies to input parameters, otherwise it return None.
        
        """
        
        rule_search = lambda node, point=point: self.__point_comparator(node.data, point)
        return self.__find_node_by_rule(point, rule_search, cur_node)