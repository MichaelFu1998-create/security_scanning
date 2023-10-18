def find_nearest_leaf(self, entry, search_node = None):
        """!
        @brief Search nearest leaf to the specified clustering feature.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): Node from that searching should be started, if None then search process will be started for the root.
        
        @return (leaf_node) Nearest node to the specified clustering feature.
        
        """
        
        if (search_node is None):
            search_node = self.__root;
        
        nearest_node = search_node;
        
        if (search_node.type == cfnode_type.CFNODE_NONLEAF):
            min_key = lambda child_node: child_node.feature.get_distance(entry, self.__type_measurement);
            nearest_child_node = min(search_node.successors, key = min_key);
            
            nearest_node = self.find_nearest_leaf(entry, nearest_child_node);
        
        return nearest_node;