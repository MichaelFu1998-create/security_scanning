def create(self):
        """Create the VBO"""
        dtype = NP_COMPONENT_DTYPE[self.component_type.value]
        data = numpy.frombuffer(
            self.buffer.read(byte_length=self.byte_length, byte_offset=self.byte_offset),
            count=self.count * self.components,
            dtype=dtype,
        )
        return dtype, data