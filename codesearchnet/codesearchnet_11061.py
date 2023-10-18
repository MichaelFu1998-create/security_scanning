def index_buffer(self, buffer, index_element_size=4):
        """
        Set the index buffer for this VAO

        Args:
            buffer: ``moderngl.Buffer``, ``numpy.array`` or ``bytes``

        Keyword Args:
            index_element_size (int): Byte size of each element. 1, 2 or 4
        """
        if not type(buffer) in [moderngl.Buffer, numpy.ndarray, bytes]:
            raise VAOError("buffer parameter must be a moderngl.Buffer, numpy.ndarray or bytes instance")

        if isinstance(buffer, numpy.ndarray):
            buffer = self.ctx.buffer(buffer.tobytes())

        if isinstance(buffer, bytes):
            buffer = self.ctx.buffer(data=buffer)

        self._index_buffer = buffer
        self._index_element_size = index_element_size