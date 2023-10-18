def BSF(cpu, dest, src):
        """
        Bit scan forward.

        Searches the source operand (second operand) for the least significant
        set bit (1 bit). If a least significant 1 bit is found, its bit index
        is stored in the destination operand (first operand). The source operand
        can be a register or a memory location; the destination operand is a register.
        The bit index is an unsigned offset from bit 0 of the source operand.
        If the contents source operand are 0, the contents of the destination
        operand is undefined::

                    IF SRC  =  0
                    THEN
                        ZF  =  1;
                        DEST is undefined;
                    ELSE
                        ZF  =  0;
                        temp  =  0;
                        WHILE Bit(SRC, temp)  =  0
                        DO
                            temp  =  temp + 1;
                            DEST  =  temp;
                        OD;
                    FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        value = src.read()
        flag = Operators.EXTRACT(value, 0, 1) == 1
        res = 0
        for pos in range(1, src.size):
            res = Operators.ITEBV(dest.size, flag, res, pos)
            flag = Operators.OR(flag, Operators.EXTRACT(value, pos, 1) == 1)

        cpu.ZF = value == 0
        dest.write(Operators.ITEBV(dest.size, cpu.ZF, dest.read(), res))