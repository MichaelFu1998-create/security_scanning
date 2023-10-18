def PSUBB(cpu, dest, src):
        """
        Packed subtract.

        Performs a SIMD subtract of the packed integers of the source operand (second operand) from the packed
        integers of the destination operand (first operand), and stores the packed integer results in the
        destination operand. The source operand can be an MMX(TM) technology register or a 64-bit memory location,
        or it can be an XMM register or a 128-bit memory location. The destination operand can be an MMX or an XMM
        register.
        The PSUBB instruction subtracts packed byte integers. When an individual result is too large or too small
        to be represented in a byte, the result is wrapped around and the low 8 bits are written to the
        destination element.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        result = []
        value_a = dest.read()
        value_b = src.read()
        for i in reversed(range(0, dest.size, 8)):
            a = Operators.EXTRACT(value_a, i, 8)
            b = Operators.EXTRACT(value_b, i, 8)
            result.append((a - b) & 0xff)
        dest.write(Operators.CONCAT(8 * len(result), *result))