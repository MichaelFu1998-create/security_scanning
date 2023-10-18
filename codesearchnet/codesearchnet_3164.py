def read_bytes(self, where, size, force=False):
        """
        Read from memory.

        :param int where: address to read data from
        :param int size: number of bytes
        :param force: whether to ignore memory permissions
        :return: data
        :rtype: list[int or Expression]
        """
        result = []
        for i in range(size):
            result.append(Operators.CHR(self.read_int(where + i, 8, force)))
        return result