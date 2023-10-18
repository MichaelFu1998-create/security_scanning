def pop(self, *args):
        """remove and return item at index (default last)."""
        value = list.pop(self, *args)
        index = self._dict.pop(value.id)
        # If the pop occured from a location other than the end of the list,
        # we will need to subtract 1 from every entry afterwards
        if len(args) == 0 or args == [-1]:  # removing from the end of the list
            return value
        _dict = self._dict
        for i, j in iteritems(_dict):
            if j > index:
                _dict[i] = j - 1
        return value