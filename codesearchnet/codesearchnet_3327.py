def MOVSD(cpu, dest, src):
        """
        Move Scalar Double-Precision Floating-Point Value

        Moves a scalar double-precision floating-point value from the source
        operand (second operand) to the destination operand (first operand).
        The source and destination operands can be XMM registers or 64-bit memory
        locations. This instruction can be used to move a double-precision
        floating-point value to and from the low quadword of an XMM register and
        a 64-bit memory location, or to move a double-precision floating-point
        value between the low quadwords of two XMM registers. The instruction
        cannot be used to transfer data between memory locations.
        When the source and destination operands are XMM registers, the high
        quadword of the destination operand remains unchanged. When the source
        operand is a memory location and destination operand is an XMM registers,
        the high quadword of the destination operand is cleared to all 0s.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        assert dest.type != 'memory' or src.type != 'memory'
        value = Operators.EXTRACT(src.read(), 0, 64)
        if dest.size > src.size:
            value = Operators.ZEXTEND(value, dest.size)
        dest.write(value)