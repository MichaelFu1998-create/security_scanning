def rename(self, key: Any, new_key: Any):
        """
        Renames an item in this collection as a transaction.

        Will override if new key name already exists.
        :param key: the current name of the item
        :param new_key: the new name that the item should have
        """
        if new_key == key:
            return

        required_locks = [self._key_locks[key], self._key_locks[new_key]]
        ordered_required_locks = sorted(required_locks, key=lambda x: id(x))
        for lock in ordered_required_locks:
            lock.acquire()

        try:
            if key not in self._data:
                raise KeyError("Attribute to rename \"%s\" does not exist" % key)
            self._data[new_key] = self[key]
            del self._data[key]
        finally:
            for lock in required_locks:
                lock.release()