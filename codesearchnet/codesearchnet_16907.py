def add_item(self, key, value, after=False, index=None, pos_key=None,
            replace=True):
        """
        Add an item at a specific location, possibly replacing the
        existing item.

        If after is True, we insert *after* the given index, otherwise we
        insert before.

        The position is specified using either index or pos_key, the former
        specifies the position from the start of the array (base 0).  pos_key
        specifies the name of another key, and positions the new key relative
        to that key.

        When replacing, the position will be left un-changed unless a location
        is specified explicitly.
        """
        if self._validate_fn:
            self._validate_fn(value)

        if (index is not None) and (pos_key is not None):
            raise ValueError('Either specify index or pos_key, not both.')
        elif pos_key is not None:
            try:
                index = self.index(pos_key)
            except ValueError:
                raise KeyError('%r not found' % pos_key)

        if after and (index is not None):
            # insert inserts *before* index, so increment by one.
            index += 1

        if key in self._values:
            if not replace:
                raise KeyError('%r is duplicate' % key)

            if index is not None:
                # We are re-locating.
                del self[key]
            else:
                # We are updating
                self._values[key] = value
                return

        if index is not None:
            # Place at given position
            self._order.insert(index, key)
        else:
            # Place at end
            self._order.append(key)
        self._values[key] = value