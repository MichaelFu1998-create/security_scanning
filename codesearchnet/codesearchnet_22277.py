def push(self, k):
        """Push k to the top of the list

        >>> l = DLL()
        >>> l.push(1)
        >>> l
        [1]
        >>> l.push(2)
        >>> l
        [2, 1]
        >>> l.push(3)
        >>> l
        [3, 2, 1]
        """
        if not self._first:
            # first item
            self._first = self._last = node = DLL.Node(k)
        elif self._first.value == k:
            # it's already at the top
            return
        else:
            try:
                self.delete(k) # in case we have it already
            except KeyError:
                pass
            self._first = node = self._first.insert_before(k)
        self._index[k] = node
        self._size += 1