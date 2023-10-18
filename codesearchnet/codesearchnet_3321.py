def POR(cpu, dest, src):
        """
        Performs a bitwise logical OR operation on the source operand (second operand) and the destination operand
        (first operand) and stores the result in the destination operand. The source operand can be an MMX technology
        register or a 64-bit memory location or it can be an XMM register or a 128-bit memory location. The destination
        operand can be an MMX technology register or an XMM register. Each bit of the result is set to 1 if either
        or both of the corresponding bits of the first and second operands are 1; otherwise, it is set to 0.
        """
        res = dest.write(dest.read() | src.read())