def push_int(self, value, force=False):
        """
        Decrement the stack pointer and write `value` to the stack.

        :param int value: The value to write
        :param force: whether to ignore memory permissions
        :return: New stack pointer
        """
        self.STACK -= self.address_bit_size // 8
        self.write_int(self.STACK, value, force=force)
        return self.STACK