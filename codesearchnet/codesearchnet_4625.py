def __find_node_by_rule(self, point, search_rule, cur_node):
        """!
        @brief Search node that satisfy to parameters in search rule.
        @details If node with specified parameters does not exist then None will be returned, 
                  otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] search_rule (lambda): Rule that is called to check whether node satisfies to search parameter.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node if it satisfies to input parameters, otherwise it return None.
        
        """
        
        req_node = None
        
        if cur_node is None:
            cur_node = self.__root
        
        while cur_node:
            if cur_node.data[cur_node.disc] <= point[cur_node.disc]:
                # Check if it's required node
                if search_rule(cur_node):
                    req_node = cur_node
                    break
                
                cur_node = cur_node.right
            
            else:
                cur_node = cur_node.left
        
        return req_node