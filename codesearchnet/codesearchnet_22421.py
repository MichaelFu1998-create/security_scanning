def runtimepath(self):
        """
        :return: runtime path of *Vim*
        :rtype: runtimepath.RuntimePath
        """
        if self._runtimepath is None:
            self._runtimepath = runtimepath.RuntimePath(self)
        return self._runtimepath