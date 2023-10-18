def union(self, iterable):
        """adds elements with id's not already in the model"""
        _dict = self._dict
        append = self.append
        for i in iterable:
            if i.id not in _dict:
                append(i)