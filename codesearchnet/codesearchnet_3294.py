def BTC(cpu, dest, src):
        """
        Bit test and complement.

        Selects the bit in a bit string (specified with the first operand, called
        the bit base) at the bit-position designated by the bit offset operand
        (second operand), stores the value of the bit in the CF flag, and complements
        the selected bit in the bit string.

        :param cpu: current CPU.
        :param dest: bit base operand.
        :param src: bit offset operand.
        """
        if dest.type == 'register':
            value = dest.read()
            pos = src.read() % dest.size
            cpu.CF = value & (1 << pos) == 1 << pos
            dest.write(value ^ (1 << pos))
        elif dest.type == 'memory':
            addr, pos = cpu._getMemoryBit(dest, src)
            base, size, ty = cpu.get_descriptor(cpu.DS)
            addr += base
            value = cpu.read_int(addr, 8)
            cpu.CF = value & (1 << pos) == 1 << pos
            value = value ^ (1 << pos)
            cpu.write_int(addr, value, 8)
        else:
            raise NotImplementedError(f"Unknown operand for BTC: {dest.type}")