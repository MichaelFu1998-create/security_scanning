def __recursive_insert(self, entry, search_node):
        """!
        @brief Recursive insert of the entry to the tree.
        @details It performs all required procedures during insertion such as splitting, merging.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): Node from that insertion should be started.
        
        @return (bool) True if number of nodes at the below level is changed, otherwise False.
        
        """
        
        # None-leaf node
        if (search_node.type == cfnode_type.CFNODE_NONLEAF):
            return self.__insert_for_noneleaf_node(entry, search_node);
        
        # Leaf is reached 
        else:
            return self.__insert_for_leaf_node(entry, search_node);