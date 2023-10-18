def insert_successor(self, successor):
        """!
        @brief Insert successor to the node.
        
        @param[in] successor (cfnode): Successor for adding.
        
        """
        
        self.feature += successor.feature;
        self.successors.append(successor);
        
        successor.parent = self;