def info(self, byte_offset=0):
        """
        Get the underlying buffer info
        :param byte_offset: byte offset from accessor
        :return: buffer, byte_length, byte_offset
        """
        return self.buffer, self.byteLength, byte_offset + self.byteOffset