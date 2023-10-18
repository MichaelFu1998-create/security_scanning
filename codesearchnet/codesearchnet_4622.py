def find_minimal_node(self, node_head, discriminator):
        """!
        @brief Find minimal node in line with coordinate that is defined by discriminator.
        
        @param[in] node_head (node): Node of KD tree from that search should be started.
        @param[in] discriminator (uint): Coordinate number that is used for comparison.
        
        @return (node) Minimal node in line with descriminator from the specified node.
        
        """
        
        min_key = lambda cur_node: cur_node.data[discriminator]
        stack = []
        candidates = []
        isFinished = False
        while isFinished is False:
            if node_head is not None:
                stack.append(node_head)
                node_head = node_head.left
            else:
                if len(stack) != 0:
                    node_head = stack.pop()
                    candidates.append(node_head)
                    node_head = node_head.right
                else:
                    isFinished = True

        return min(candidates, key = min_key)