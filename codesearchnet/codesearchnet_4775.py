def get_level_nodes(self, level):
        """!
        @brief Traverses CF-tree to obtain nodes at the specified level.
        
        @param[in] level (uint): CF-tree level from that nodes should be returned.
        
        @return (list) List of CF-nodes that are located on the specified level of the CF-tree.
        
        """
        
        level_nodes = [];
        if (level < self.__height):
            level_nodes = self.__recursive_get_level_nodes(level, self.__root);
        
        return level_nodes;