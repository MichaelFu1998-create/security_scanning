def sort(self, cmp=None, key=None, reverse=False):
        """stable sort *IN PLACE*

        cmp(x, y) -> -1, 0, 1

        """
        if key is None:
            def key(i):
                return i.id
        if PY3:
            list.sort(self, key=key, reverse=reverse)
        else:
            list.sort(self, cmp=cmp, key=key, reverse=reverse)
        self._generate_index()