def merge(self, node):
        """!
        @brief Merge non-leaf node to the current.
        
        @param[in] node (non_leaf_node): Non-leaf node that should be merged with current.
        
        """
                
        self.feature += node.feature;
        
        for child in node.successors:
            child.parent = self;
            self.successors.append(child);