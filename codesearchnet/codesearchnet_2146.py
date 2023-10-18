def _sample_with_priority(self, p):
        """
        Sample random element with priority greater than p.
        """
        parent = 0
        while True:
            left = 2 * parent + 1
            if left >= len(self._memory):
                # parent points to a leaf node already.
                return parent

            left_p = self._memory[left] if left < self._capacity - 1 \
                else (self._memory[left].priority or 0)
            if p <= left_p:
                parent = left
            else:
                if left + 1 >= len(self._memory):
                    raise RuntimeError('Right child is expected to exist.')
                p -= left_p
                parent = left + 1