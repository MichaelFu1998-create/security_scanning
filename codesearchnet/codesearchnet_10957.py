def info(self):
        """
        Get underlying buffer info for this accessor
        :return: buffer, byte_length, byte_offset, component_type, count
        """
        buffer, byte_length, byte_offset = self.bufferView.info(byte_offset=self.byteOffset)
        return buffer, self.bufferView, \
            byte_length, byte_offset, \
            self.componentType, ACCESSOR_TYPE[self.type], self.count