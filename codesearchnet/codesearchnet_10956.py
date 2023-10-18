def read(self):
        """
        Reads buffer data
        :return: component count, component type, data
        """
        # ComponentType helps us determine the datatype
        dtype = NP_COMPONENT_DTYPE[self.componentType.value]
        return ACCESSOR_TYPE[self.type], self.componentType, self.bufferView.read(
            byte_offset=self.byteOffset,
            dtype=dtype,
            count=self.count * ACCESSOR_TYPE[self.type],
        )