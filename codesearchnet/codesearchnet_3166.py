def read_string(self, where, max_length=None, force=False):
        """
        Read a NUL-terminated concrete buffer from memory. Stops reading at first symbolic byte.

        :param int where: Address to read string from
        :param int max_length:
            The size in bytes to cap the string at, or None [default] for no
            limit.
        :param force: whether to ignore memory permissions
        :return: string read
        :rtype: str
        """
        s = io.BytesIO()
        while True:
            c = self.read_int(where, 8, force)

            if issymbolic(c) or c == 0:
                break

            if max_length is not None:
                if max_length == 0:
                    break
                max_length = max_length - 1
            s.write(Operators.CHR(c))
            where += 1
        return s.getvalue().decode()