def screen_size(self, size):
        """
        :param size: (lines, columns) tuple of a screen connected to *Vim*.
        :type size: (int, int)
        """
        if self.screen_size != size:
            self._screen.resize(*self._swap(size))