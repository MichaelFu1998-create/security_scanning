def LODS(cpu, dest, src):
        """
        Loads string.

        Loads a byte, word, or doubleword from the source operand into the AL, AX, or EAX register, respectively. The
        source operand is a memory location, the address of which is read from the DS:ESI or the DS:SI registers
        (depending on the address-size attribute of the instruction, 32 or 16, respectively). The DS segment may be over-
        ridden with a segment override prefix.
        After the byte, word, or doubleword is transferred from the memory location into the AL, AX, or EAX register, the
        (E)SI register is incremented or decremented automatically according to the setting of the DF flag in the EFLAGS
        register. (If the DF flag is 0, the (E)SI register is incremented; if the DF flag is 1, the ESI register is decremented.)
        The (E)SI register is incremented or decremented by 1 for byte operations, by 2 for word operations, or by 4 for
        doubleword operations.

        :param cpu: current CPU.
        :param dest: source operand.
        """
        src_reg = {8: 'SI', 32: 'ESI', 64: 'RSI'}[cpu.address_bit_size]
        base, _, ty = cpu.get_descriptor(cpu.DS)

        src_addr = cpu.read_register(src_reg) + base
        size = dest.size

        arg0 = cpu.read_int(src_addr, size)
        dest.write(arg0)

        increment = Operators.ITEBV(cpu.address_bit_size, cpu.DF, -size // 8, size // 8)
        cpu.write_register(src_reg, cpu.read_register(src_reg) + increment)