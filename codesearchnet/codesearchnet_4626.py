def find_node_with_payload(self, point, point_payload, cur_node = None):
        """!
        @brief Find node with specified coordinates and payload.
        @details If node with specified parameters does not exist then None will be returned, 
                  otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] point_payload (any): Payload of the node that is searched in the tree.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node if it satisfies to input parameters, otherwise it return None.
        
        """
        
        rule_search = lambda node, point=point, payload=point_payload: self.__point_comparator(node.data, point) and node.payload == payload
        return self.__find_node_by_rule(point, rule_search, cur_node)