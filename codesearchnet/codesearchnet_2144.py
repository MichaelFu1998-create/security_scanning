def _update_internal_nodes(self, index, delta):
        """
        Update internal priority sums when leaf priority has been changed.
        Args:
            index: leaf node index
            delta: change in priority
        """
        # Move up tree, increasing position, updating sum
        while index > 0:
            index = (index - 1) // 2
            self._memory[index] += delta