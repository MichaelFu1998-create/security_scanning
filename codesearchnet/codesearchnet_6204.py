def get_by_any(self, iterable):
        """
        Get a list of members using several different ways of indexing

        Parameters
        ----------
        iterable : list (if not, turned into single element list)
            list where each element is either int (referring to an index in
            in this DictList), string (a id of a member in this DictList) or
            member of this DictList for pass-through

        Returns
        -------
        list
            a list of members
        """
        def get_item(item):
            if isinstance(item, int):
                return self[item]
            elif isinstance(item, string_types):
                return self.get_by_id(item)
            elif item in self:
                return item
            else:
                raise TypeError("item in iterable cannot be '%s'" % type(item))

        if not isinstance(iterable, list):
            iterable = [iterable]
        return [get_item(item) for item in iterable]