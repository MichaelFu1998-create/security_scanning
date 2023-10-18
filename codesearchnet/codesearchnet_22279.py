def pop(self):
        """
        >>> l = DLL()
        >>> l.push(1)
        >>> l.pop()
        1
        """
        k = self._last.value
        self.deletenode(self._last)
        return k