def write(self, path):
        """Write buffer to file"""

        with open(path, "wb") as fout:
            fout.write(self.m_buf)