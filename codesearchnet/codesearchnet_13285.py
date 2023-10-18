def get_items_by_group(self, group, case_sensitive = True):
        """
        Return a list of items within a given group.

        :Parameters:
            - `name`: name to look-up
            - `case_sensitive`: if `False` the matching will be case
              insensitive.
        :Types:
            - `name`: `unicode`
            - `case_sensitive`: `bool`

        :Returntype: `list` of `RosterItem`
        """
        result = []
        if not group:
            for item in self._items:
                if not item.groups:
                    result.append(item)
            return result
        if not case_sensitive:
            group = group.lower()
        for item in self._items:
            if group in item.groups:
                result.append(item)
            elif not case_sensitive and group in [g.lower() for g
                                                            in item.groups]:
                result.append(item)
        return result