def __split_nonleaf_node(self, node):
        """!
        @brief Performs splitting of the specified non-leaf node.
        
        @param[in] node (non_leaf_node): Non-leaf node that should be splitted.
        
        @return (list) New pair of non-leaf nodes [non_leaf_node1, non_leaf_node2].
        
        """
        
        [farthest_node1, farthest_node2] = node.get_farthest_successors(self.__type_measurement);
        
        # create new non-leaf nodes
        new_node1 = non_leaf_node(farthest_node1.feature, node.parent, [ farthest_node1 ], None);
        new_node2 = non_leaf_node(farthest_node2.feature, node.parent, [ farthest_node2 ], None);
        
        farthest_node1.parent = new_node1;
        farthest_node2.parent = new_node2;
        
        # re-insert other successors
        for successor in node.successors:
            if ( (successor is not farthest_node1) and (successor is not farthest_node2) ):
                distance1 = new_node1.get_distance(successor, self.__type_measurement);
                distance2 = new_node2.get_distance(successor, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.insert_successor(successor);
                else:
                    new_node2.insert_successor(successor);
        
        return [new_node1, new_node2];