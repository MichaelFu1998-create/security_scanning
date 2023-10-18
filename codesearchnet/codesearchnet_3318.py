def MOVLPD(cpu, dest, src):
        """
        Moves low packed double-precision floating-point value.

        Moves a double-precision floating-point value from the source operand (second operand) and the
        destination operand (first operand). The source and destination operands can be an XMM register
        or a 64-bit memory location. This instruction allows double-precision floating-point values to be moved
        to and from the low quadword of an XMM register and memory. It cannot be used for register to register
        or memory to memory moves. When the destination operand is an XMM register, the high quadword of the
        register remains unchanged.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        value = src.read()
        if src.size == 64 and dest.size == 128:
            value = (dest.read() & 0xffffffffffffffff0000000000000000) | Operators.ZEXTEND(value, 128)
        dest.write(value)