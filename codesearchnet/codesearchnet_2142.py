def move(self, external_index, new_priority):
        """
        Change the priority of a leaf node
        """
        index = external_index + (self._capacity - 1)
        return self._move(index, new_priority)