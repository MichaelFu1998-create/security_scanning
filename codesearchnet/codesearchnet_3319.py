def MOVHPD(cpu, dest, src):
        """
        Moves high packed double-precision floating-point value.

        Moves a double-precision floating-point value from the source operand (second operand) and the
        destination operand (first operand). The source and destination operands can be an XMM register
        or a 64-bit memory location. This instruction allows double-precision floating-point values to be moved
        to and from the high quadword of an XMM register and memory. It cannot be used for register to
        register or memory to memory moves. When the destination operand is an XMM register, the low quadword
        of the register remains unchanged.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        if src.size == 128:
            assert dest.size == 64
            dest.write(Operators.EXTRACT(src.read(), 64, 64))
        else:
            assert src.size == 64 and dest.size == 128
            value = Operators.EXTRACT(dest.read(), 0, 64)  # low part
            dest.write(Operators.CONCAT(128, src.read(), value))