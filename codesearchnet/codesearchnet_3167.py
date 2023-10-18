def push_bytes(self, data, force=False):
        """
        Write `data` to the stack and decrement the stack pointer accordingly.

        :param str data: Data to write
        :param force: whether to ignore memory permissions
        """
        self.STACK -= len(data)
        self.write_bytes(self.STACK, data, force)
        return self.STACK