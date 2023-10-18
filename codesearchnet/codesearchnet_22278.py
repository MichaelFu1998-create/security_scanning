def deletenode(self, node):
        """
        >>> l = DLL()
        >>> l.push(1)
        >>> l
        [1]
        >>> l.size()
        1
        >>> l.deletenode(l._first)
        >>> l
        []
        >>> l.size()
        0
        >>> l._index
        {}
        >>> l._first
        """
        if self._last == node:
            self._last = node.previous
        if self._first == node:
            self._first = node.next
        node.pop()
        del self._index[node.value]
        self._size -= 1