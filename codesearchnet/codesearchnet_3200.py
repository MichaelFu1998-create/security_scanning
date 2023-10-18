def CMPXCHG(cpu, dest, src):
        """
        Compares and exchanges.

        Compares the value in the AL, AX, EAX or RAX register (depending on the
        size of the operand) with the first operand (destination operand). If
        the two values are equal, the second operand (source operand) is loaded
        into the destination operand. Otherwise, the destination operand is
        loaded into the AL, AX, EAX or RAX register.

        The ZF flag is set if the values in the destination operand and
        register AL, AX, or EAX are equal; otherwise it is cleared. The CF, PF,
        AF, SF, and OF flags are set according to the results of the comparison
        operation::

        (* accumulator  =  AL, AX, EAX or RAX,  depending on whether *)
        (* a byte, word, a doubleword or a 64bit comparison is being performed*)
        IF accumulator  ==  DEST
        THEN
            ZF  =  1
            DEST  =  SRC
        ELSE
            ZF  =  0
            accumulator  =  DEST
        FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        size = dest.size
        reg_name = {8: 'AL', 16: 'AX', 32: 'EAX', 64: 'RAX'}[size]
        accumulator = cpu.read_register(reg_name)
        sval = src.read()
        dval = dest.read()

        cpu.write_register(reg_name, dval)
        dest.write(Operators.ITEBV(size, accumulator == dval, sval, dval))

        # Affected Flags o..szapc
        cpu._calculate_CMP_flags(size, accumulator - dval, accumulator, dval)