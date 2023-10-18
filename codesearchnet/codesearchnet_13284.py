def get_items_by_name(self, name, case_sensitive = True):
        """
        Return a list of items with given name.

        :Parameters:
            - `name`: name to look-up
            - `case_sensitive`: if `False` the matching will be case
              insensitive.
        :Types:
            - `name`: `unicode`
            - `case_sensitive`: `bool`

        :Returntype: `list` of `RosterItem`
        """
        if not case_sensitive and name:
            name = name.lower()
        result = []
        for item in self._items:
            if item.name == name:
                result.append(item)
            elif item.name is None:
                continue
            elif not case_sensitive and item.name.lower() == name:
                result.append(item)
        return result