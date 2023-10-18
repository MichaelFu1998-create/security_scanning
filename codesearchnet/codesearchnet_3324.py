def VORPS(cpu, dest, src, src2):
        """
        Performs a bitwise logical OR operation on the source operand (second operand) and second source operand (third operand)
         and stores the result in the destination operand (first operand).
        """
        res = dest.write(src.read() | src2.read())