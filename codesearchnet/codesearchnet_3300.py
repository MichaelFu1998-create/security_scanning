def STOS(cpu, dest, src):
        """
        Stores String.

        Stores a byte, word, or doubleword from the AL, AX, or EAX register,
        respectively, into the destination operand. The destination operand is
        a memory location, the address of which is read from either the ES:EDI
        or the ES:DI registers (depending on the address-size attribute of the
        instruction, 32 or 16, respectively). The ES segment cannot be overridden
        with a segment override prefix.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        size = src.size
        dest.write(src.read())
        dest_reg = dest.mem.base
        increment = Operators.ITEBV({'RDI': 64, 'EDI': 32, 'DI': 16}[dest_reg], cpu.DF, -size // 8, size // 8)
        cpu.write_register(dest_reg, cpu.read_register(dest_reg) + increment)