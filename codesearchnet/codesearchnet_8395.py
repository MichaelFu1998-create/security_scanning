def dump(self, offset=0, length=1):
        """Dump item"""

        for i in range(offset, offset + length):
            if "ctypes" in str(self.m_types):
                cij.info("Buff[%s]: %s" % (i, self.m_buf[i]))
            else:
                cij.info("Buff[%s]:" % i)
                dump(self.m_buf[i], 2)