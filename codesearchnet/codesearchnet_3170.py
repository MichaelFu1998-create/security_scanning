def pop_int(self, force=False):
        """
        Read a value from the stack and increment the stack pointer.

        :param force: whether to ignore memory permissions
        :return: Value read
        """
        value = self.read_int(self.STACK, force=force)
        self.STACK += self.address_bit_size // 8
        return value