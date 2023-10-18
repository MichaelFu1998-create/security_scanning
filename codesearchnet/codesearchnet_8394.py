def read(self, path):
        """Read file to buffer"""

        with open(path, "rb") as fout:
            memmove(self.m_buf, fout.read(self.m_size), self.m_size)