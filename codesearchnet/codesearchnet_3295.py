def POPCNT(cpu, dest, src):
        """
        This instruction calculates of number of bits set to 1 in the second
        operand (source) and returns the count in the first operand (a destination
        register).
        Count = 0;
        For (i=0; i < OperandSize; i++) {
            IF (SRC[ i] = 1) // i'th bit
                THEN Count++;
            FI;
        }
        DEST = Count;
        Flags Affected
        OF, SF, ZF, AF, CF, PF are all cleared.
        ZF is set if SRC = 0, otherwise ZF is cleared
        """
        count = 0
        source = src.read()
        for i in range(src.size):
            count += Operators.ITEBV(dest.size, (source >> i) & 1 == 1, 1, 0)
        dest.write(count)
        # Flags
        cpu.OF = False
        cpu.SF = False
        cpu.AF = False
        cpu.CF = False
        cpu.PF = False
        cpu.ZF = source == 0