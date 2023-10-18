def insert(self, index, object):
        """insert object before index"""
        self._check(object.id)
        list.insert(self, index, object)
        # all subsequent entries now have been shifted up by 1
        _dict = self._dict
        for i, j in iteritems(_dict):
            if j >= index:
                _dict[i] = j + 1
        _dict[object.id] = index