def __recursive_get_level_nodes(self, level, node):
        """!
        @brief Traverses CF-tree to obtain nodes at the specified level recursively.
        
        @param[in] level (uint): Current CF-tree level.
        @param[in] node (cfnode): CF-node from that traversing is performed.
        
        @return (list) List of CF-nodes that are located on the specified level of the CF-tree.
        
        """
        
        level_nodes = [];
        if (level is 0):
            level_nodes.append(node);
        
        else:
            for sucessor in node.successors:
                level_nodes += self.__recursive_get_level_nodes(level - 1, sucessor);
        
        return level_nodes;