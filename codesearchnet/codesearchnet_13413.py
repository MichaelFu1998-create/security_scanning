def _try_backup_item(self):
        """Check if a backup item is available in cache and call
        the item handler if it is.

        :return: `True` if backup item was found.
        :returntype: `bool`"""
        if not self._backup_state:
            return False
        item = self.cache.get_item(self.address, self._backup_state)
        if item:
            self._object_handler(item.address, item.value, item.state)
            return True
        else:
            False