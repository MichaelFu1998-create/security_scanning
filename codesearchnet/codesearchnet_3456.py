def seek(self, offset, whence=os.SEEK_SET):
        """
        Repositions the file C{offset} according to C{whence}.
        Returns the resulting offset or -1 in case of error.
        :rtype: int
        :return: the file offset.
        """
        assert isinstance(offset, int)
        assert whence in (os.SEEK_SET, os.SEEK_CUR, os.SEEK_END)

        new_position = 0
        if whence == os.SEEK_SET:
            new_position = offset
        elif whence == os.SEEK_CUR:
            new_position = self.pos + offset
        elif whence == os.SEEK_END:
            new_position = self.max_size + offset

        if new_position < 0:
            return -1

        self.pos = new_position

        return self.pos