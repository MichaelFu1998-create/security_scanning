def remove_successor(self, successor):
        """!
        @brief Remove successor from the node.
        
        @param[in] successor (cfnode): Successor for removing.
        
        """
        
        self.feature -= successor.feature;
        self.successors.append(successor);
        
        successor.parent = self;