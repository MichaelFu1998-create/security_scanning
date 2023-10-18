def add_item(self, item, replace = False):
        """
        Add an item to the roster.

        This will not automatically update the roster on the server.

        :Parameters:
            - `item`: the item to add
            - `replace`: if `True` then existing item will be replaced,
              otherwise a `ValueError` will be raised on conflict
        :Types:
            - `item`: `RosterItem`
            - `replace`: `bool`
        """
        if item.jid in self._jids:
            if replace:
                self.remove_item(item.jid)
            else:
                raise ValueError("JID already in the roster")
        index = len(self._items)
        self._items.append(item)
        self._jids[item.jid] = index