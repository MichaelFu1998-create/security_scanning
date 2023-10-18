def _readblock(self):
        """Read a block from the server. Lines are read until a character ``.`` is found

        :return: the read block
        :rtype: string

        """
        block = ''
        while not self._stop:
            line = self._readline()
            if line == '.':
                break
            block += line
        return block