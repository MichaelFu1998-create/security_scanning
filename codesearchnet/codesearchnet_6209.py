def extend(self, iterable):
        """extend list by appending elements from the iterable"""
        # Sometimes during initialization from an older pickle, _dict
        # will not have initialized yet, because the initialization class was
        # left unspecified. This is an issue because unpickling calls
        # DictList.extend, which requires the presence of _dict. Therefore,
        # the issue is caught and addressed here.
        if not hasattr(self, "_dict") or self._dict is None:
            self._dict = {}
        _dict = self._dict
        current_length = len(self)
        list.extend(self, iterable)
        for i, obj in enumerate(islice(self, current_length, None),
                                current_length):
            the_id = obj.id
            if the_id not in _dict:
                _dict[the_id] = i
            else:
                # undo the extend and raise an error
                self = self[:current_length]
                self._check(the_id)
                # if the above succeeded, then the id must be present
                # twice in the list being added
                raise ValueError("id '%s' at index %d is non-unique. "
                                 "Is it present twice?" % (str(the_id), i))