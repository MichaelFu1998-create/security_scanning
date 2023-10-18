def set_colors(self, buf):
        """
        DEPRECATED: use self.color_list

        Use with extreme caution!
        Directly sets the internal buffer and bypasses all brightness and
        rotation control buf must also be in the exact format required by the
        display type.
        """
        deprecated.deprecated('layout.set_colors')
        if len(self._colors) != len(buf):
            raise IOError("Data buffer size incorrect! "
                          "Expected: {} bytes / Received: {} bytes"
                          .format(len(self._colors), len(buf)))
        self._colors[:] = buf