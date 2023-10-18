def MOVS(cpu, dest, src):
        """
        Moves data from string to string.

        Moves the byte, word, or doubleword specified with the second operand (source operand) to the location specified
        with the first operand (destination operand). Both the source and destination operands are located in memory. The
        address of the source operand is read from the DS:ESI or the DS:SI registers (depending on the address-size
        attribute of the instruction, 32 or 16, respectively). The address of the destination operand is read from the ES:EDI
        or the ES:DI registers (again depending on the address-size attribute of the instruction). The DS segment may be
        overridden with a segment override prefix, but the ES segment cannot be overridden.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        base, size, ty = cpu.get_descriptor(cpu.DS)
        src_addr = src.address() + base
        dest_addr = dest.address() + base

        src_reg = src.mem.base
        dest_reg = dest.mem.base
        size = dest.size

        # Copy the data
        dest.write(src.read())

        #Advance EDI/ESI pointers
        increment = Operators.ITEBV(cpu.address_bit_size, cpu.DF, -size // 8, size // 8)
        cpu.write_register(src_reg, cpu.read_register(src_reg) + increment)
        cpu.write_register(dest_reg, cpu.read_register(dest_reg) + increment)