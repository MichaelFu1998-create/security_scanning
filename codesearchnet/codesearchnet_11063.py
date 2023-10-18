def release(self, buffer=True):
        """
        Destroy the vao object

        Keyword Args:
            buffers (bool): also release buffers
        """
        for key, vao in self.vaos:
            vao.release()

        if buffer:
            for buff in self.buffers:
                buff.buffer.release()

            if self._index_buffer:
                self._index_buffer.release()