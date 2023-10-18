def _fix_index(self, index):
        """
        :param slice index:
        """
        stop, start = index.stop, index.start
        if start is None:
            start = 0
        if stop is None:
            stop = len(self)
        return start, stop