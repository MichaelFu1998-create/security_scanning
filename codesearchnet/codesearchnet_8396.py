def compare(self, buf, offset=0, length=1, ignore=""):
        """Compare buffer"""

        for i in range(offset, offset + length):
            if isinstance(self.m_types, (type(Union), type(Structure))):
                if compare(self.m_buf[i], buf[i], ignore=ignore):
                    return 1
            elif self.m_buf[i] != buf[i]:
                return 1

        return 0