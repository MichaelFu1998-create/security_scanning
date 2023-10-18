def traverse(self, start_node = None, level = None):
        """!
        @brief Traverses all nodes of subtree that is defined by node specified in input parameter.
        
        @param[in] start_node (node): Node from that travering of subtree is performed.
        @param[in, out] level (uint): Should be ignored by application.
        
        @return (list) All nodes of the subtree.
        
        """
        
        if start_node is None:
            start_node  = self.__root
            level = 0
        
        if start_node is None:
            return []
        
        items = [ (level, start_node) ]
        for child in self.children(start_node):
            if child is not None:
                items += self.traverse(child, level + 1)
        
        return items