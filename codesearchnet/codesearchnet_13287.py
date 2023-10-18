def remove_item(self, jid):
        """Remove item from the roster.

        :Parameters:
            - `jid`: JID of the item to remove
        :Types:
            - `jid`: `JID`
        """
        if jid not in self._jids:
            raise KeyError(jid)
        index = self._jids[jid]
        for i in range(index, len(self._jids)):
            self._jids[self._items[i].jid] -= 1
        del self._jids[jid]
        del self._items[index]