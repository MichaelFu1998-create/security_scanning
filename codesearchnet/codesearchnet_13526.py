def expire(self):
        """Do the expiration of dictionary items.

        Remove items that expired by now from the dictionary.

        :Return: time, in seconds, when the next item expires or `None`
        :returntype: `float`
        """
        with self._lock:
            logger.debug("expdict.expire. timeouts: {0!r}"
                                                    .format(self._timeouts))
            next_timeout = None
            for k in self._timeouts.keys():
                ret = self._expire_item(k)
                if ret is not None:
                    if next_timeout is None:
                        next_timeout = ret
                    else:
                        next_timeout = min(next_timeout, ret)
            return next_timeout