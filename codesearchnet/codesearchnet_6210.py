def _extend_nocheck(self, iterable):
        """extends without checking for uniqueness

        This function should only be used internally by DictList when it
        can guarantee elements are already unique (as in when coming from
        self or other DictList). It will be faster because it skips these
        checks.

        """
        current_length = len(self)
        list.extend(self, iterable)
        _dict = self._dict
        if current_length is 0:
            self._generate_index()
            return
        for i, obj in enumerate(islice(self, current_length, None),
                                current_length):
            _dict[obj.id] = i