def push(cpu, value, size):
        """
        Writes a value in the stack.

        :param value: the value to put in the stack.
        :param size: the size of the value.
        """
        assert size in (8, 16, cpu.address_bit_size)
        cpu.STACK = cpu.STACK - size // 8
        base, _, _ = cpu.get_descriptor(cpu.read_register('SS'))
        address = cpu.STACK + base
        cpu.write_int(address, value, size)