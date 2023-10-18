def write_bytes(self, where, data, force=False):
        """
        Write a concrete or symbolic (or mixed) buffer to memory

        :param int where: address to write to
        :param data: data to write
        :type data: str or list
        :param force: whether to ignore memory permissions
        """

        mp = self.memory.map_containing(where)
        # TODO (ehennenfent) - fast write can have some yet-unstudied unintended side effects.
        # At the very least, using it in non-concrete mode will break the symbolic strcmp/strlen models. The 1024 byte
        # minimum is intended to minimize the potential effects of this by ensuring that if there _are_ any other
        # issues, they'll only crop up when we're doing very large writes, which are fairly uncommon.
        can_write_raw = type(mp) is AnonMap and \
            isinstance(data, (str, bytes)) and \
            (mp.end - mp.start + 1) >= len(data) >= 1024 and \
            not issymbolic(data) and \
            self._concrete

        if can_write_raw:
            logger.debug("Using fast write")
            offset = mp._get_offset(where)
            if isinstance(data, str):
                data = bytes(data.encode('utf-8'))
            mp._data[offset:offset + len(data)] = data
            self._publish('did_write_memory', where, data, 8 * len(data))
        else:
            for i in range(len(data)):
                self.write_int(where + i, Operators.ORD(data[i]), 8, force)