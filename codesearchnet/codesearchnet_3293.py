def BT(cpu, dest, src):
        """
        Bit Test.

        Selects the bit in a bit string (specified with the first operand, called the bit base) at the
        bit-position designated by the bit offset (specified by the second operand) and stores the value
        of the bit in the CF flag. The bit base operand can be a register or a memory location; the bit
        offset operand can be a register or an immediate value:
            - If the bit base operand specifies a register, the instruction takes the modulo 16, 32, or 64
              of the bit offset operand (modulo size depends on the mode and register size; 64-bit operands
              are available only in 64-bit mode).
            - If the bit base operand specifies a memory location, the operand represents the address of the
              byte in memory that contains the bit base (bit 0 of the specified byte) of the bit string. The
              range of the bit position that can be referenced by the offset operand depends on the operand size.

        :param cpu: current CPU.
        :param dest: bit base.
        :param src: bit offset.
        """
        if dest.type == 'register':
            cpu.CF = ((dest.read() >> (src.read() % dest.size)) & 1) != 0
        elif dest.type == 'memory':
            addr, pos = cpu._getMemoryBit(dest, src)
            base, size, ty = cpu.get_descriptor(cpu.DS)
            value = cpu.read_int(addr + base, 8)
            cpu.CF = Operators.EXTRACT(value, pos, 1) == 1
        else:
            raise NotImplementedError(f"Unknown operand for BT: {dest.type}")