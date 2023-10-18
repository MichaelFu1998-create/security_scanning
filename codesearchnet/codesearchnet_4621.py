def __recursive_remove(self, node_removed):
        """!
        @brief Delete node and return root of subtree.
        
        @param[in] node_removed (node): Node that should be removed.
        
        @return (node) Minimal node in line with coordinate that is defined by descriminator.
        
        """
                
        # Check if it is leaf
        if (node_removed.right is None) and (node_removed.left is None):
            return None
        
        discriminator = node_removed.disc
        
        # Check if only left branch exist
        if node_removed.right is None:
            node_removed.right = node_removed.left
            node_removed.left = None
        
        # Find minimal node in line with coordinate that is defined by discriminator
        minimal_node = self.find_minimal_node(node_removed.right, discriminator)
        parent = minimal_node.parent
        
        if parent.left is minimal_node:
            parent.left = self.__recursive_remove(minimal_node)
        elif parent.right is minimal_node:
            parent.right = self.__recursive_remove(minimal_node)
        
        minimal_node.parent = node_removed.parent
        minimal_node.disc = node_removed.disc
        minimal_node.right = node_removed.right
        minimal_node.left = node_removed.left
        
        # Update parent for successors of previous parent.
        if minimal_node.right is not None:
            minimal_node.right.parent = minimal_node
             
        if minimal_node.left is not None:
            minimal_node.left.parent = minimal_node
        
        return minimal_node