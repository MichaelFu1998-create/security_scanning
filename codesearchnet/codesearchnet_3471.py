def sys_access(self, buf, mode):
        """
        Checks real user's permissions for a file
        :rtype: int

        :param buf: a buffer containing the pathname to the file to check its permissions.
        :param mode: the access permissions to check.
        :return:
            -  C{0} if the calling process can access the file in the desired mode.
            - C{-1} if the calling process can not access the file in the desired mode.
        """
        filename = b''
        for i in range(0, 255):
            c = Operators.CHR(self.current.read_int(buf + i, 8))
            if c == b'\x00':
                break
            filename += c

        if os.access(filename, mode):
            return 0
        else:
            return -1