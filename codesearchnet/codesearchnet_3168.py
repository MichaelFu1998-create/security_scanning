def pop_bytes(self, nbytes, force=False):
        """
        Read `nbytes` from the stack, increment the stack pointer, and return
        data.

        :param int nbytes: How many bytes to read
        :param force: whether to ignore memory permissions
        :return: Data read from the stack
        """
        data = self.read_bytes(self.STACK, nbytes, force=force)
        self.STACK += nbytes
        return data