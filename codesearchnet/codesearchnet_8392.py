def memcopy(self, stream, offset=0, length=float("inf")):
        """Copy stream to buffer"""
        data = [ord(i) for i in list(stream)]
        size = min(length, len(data), self.m_size)
        buff = cast(self.m_buf, POINTER(c_uint8))
        for i in range(size):
            buff[offset + i] = data[i]