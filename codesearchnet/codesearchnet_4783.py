def __merge_nearest_successors(self, node):
        """!
        @brief Find nearest sucessors and merge them.
        
        @param[in] node (non_leaf_node): Node whose two nearest successors should be merged.
        
        @return (bool): True if merging has been successfully performed, otherwise False.
        
        """
        
        merging_result = False;
        
        if (node.successors[0].type == cfnode_type.CFNODE_NONLEAF):
            [nearest_child_node1, nearest_child_node2] = node.get_nearest_successors(self.__type_measurement);
            
            if (len(nearest_child_node1.successors) + len(nearest_child_node2.successors) <= self.__branch_factor):
                node.successors.remove(nearest_child_node2);
                if (nearest_child_node2.type == cfnode_type.CFNODE_LEAF):
                    self.__leafes.remove(nearest_child_node2);
                
                nearest_child_node1.merge(nearest_child_node2);
                
                merging_result = True;
        
        return merging_result;