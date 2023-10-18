def append(self, object):
        """append object to end"""
        the_id = object.id
        self._check(the_id)
        self._dict[the_id] = len(self)
        list.append(self, object)