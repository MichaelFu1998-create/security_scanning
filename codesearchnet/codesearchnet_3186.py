def pop(cpu, size):
        """
        Gets a value from the stack.

        :rtype: int
        :param size: the size of the value to consume from the stack.
        :return: the value from the stack.
        """
        assert size in (16, cpu.address_bit_size)
        base, _, _ = cpu.get_descriptor(cpu.SS)
        address = cpu.STACK + base
        value = cpu.read_int(address, size)
        cpu.STACK = cpu.STACK + size // 8
        return value