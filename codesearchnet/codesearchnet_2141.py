def put(self, item, priority=None):
        """
        Stores a transition in replay memory.

        If the memory is full, the oldest entry is replaced.
        """
        if not self._isfull():
            self._memory.append(None)
        position = self._next_position_then_increment()
        old_priority = 0 if self._memory[position] is None \
            else (self._memory[position].priority or 0)
        row = _SumRow(item, priority)
        self._memory[position] = row
        self._update_internal_nodes(
            position, (row.priority or 0) - old_priority)