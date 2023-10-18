def buffer(self, buffer, buffer_format: str, attribute_names, per_instance=False):
        """
        Register a buffer/vbo for the VAO. This can be called multiple times.
        adding multiple buffers (interleaved or not)

        Args:
            buffer: The buffer data. Can be ``numpy.array``, ``moderngl.Buffer`` or ``bytes``.
            buffer_format (str): The format of the buffer. (eg. ``3f 3f`` for interleaved positions and normals).
            attribute_names: A list of attribute names this buffer should map to.

        Keyword Args:
            per_instance (bool): Is this buffer per instance data for instanced rendering?

        Returns:
            The ``moderngl.Buffer`` instance object. This is handy when providing ``bytes`` and ``numpy.array``.
        """
        if not isinstance(attribute_names, list):
            attribute_names = [attribute_names, ]

        if not type(buffer) in [moderngl.Buffer, numpy.ndarray, bytes]:
            raise VAOError(
                (
                    "buffer parameter must be a moderngl.Buffer, numpy.ndarray or bytes instance"
                    "(not {})".format(type(buffer))
                )
            )

        if isinstance(buffer, numpy.ndarray):
            buffer = self.ctx.buffer(buffer.tobytes())

        if isinstance(buffer, bytes):
            buffer = self.ctx.buffer(data=buffer)

        formats = buffer_format.split()
        if len(formats) != len(attribute_names):
            raise VAOError("Format '{}' does not describe attributes {}".format(buffer_format, attribute_names))

        self.buffers.append(BufferInfo(buffer, buffer_format, attribute_names, per_instance=per_instance))
        self.vertex_count = self.buffers[-1].vertices

        return buffer