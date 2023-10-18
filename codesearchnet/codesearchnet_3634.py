def _UXT(cpu, dest, src, src_width):
        """
        Helper for UXT* family of instructions.

        :param ARMv7Operand dest: the destination register; register
        :param ARMv7Operand dest: the source register; register
        :param int src_width: bits to consider of the src operand
        """
        val = GetNBits(src.read(), src_width)
        word = Operators.ZEXTEND(val, cpu.address_bit_size)
        dest.write(word)