def DIV(cpu, src):
        """
        Unsigned divide.

        Divides (unsigned) the value in the AX register, DX:AX register pair,
        or EDX:EAX or RDX:RAX register pair (dividend) by the source operand
        (divisor) and stores the result in the AX (AH:AL), DX:AX, EDX:EAX or
        RDX:RAX registers. The source operand can be a general-purpose register
        or a memory location. The action of this instruction depends of the
        operand size (dividend/divisor). Division using 64-bit operand is
        available only in 64-bit mode. Non-integral results are truncated
        (chopped) towards 0. The reminder is always less than the divisor in
        magnitude. Overflow is indicated with the #DE (divide error) exception
        rather than with the CF flag::

            IF SRC  =  0
                THEN #DE; FI;(* divide error *)
            IF OperandSize  =  8 (* word/byte operation *)
                THEN
                    temp  =  AX / SRC;
                    IF temp > FFH
                        THEN #DE; (* divide error *) ;
                        ELSE
                            AL  =  temp;
                            AH  =  AX MOD SRC;
                    FI;
                ELSE IF OperandSize  =  16 (* doubleword/word operation *)
                    THEN
                        temp  =  DX:AX / SRC;
                        IF temp > FFFFH
                            THEN #DE; (* divide error *) ;
                        ELSE
                            AX  =  temp;
                            DX  =  DX:AX MOD SRC;
                        FI;
                    FI;
                ELSE If OperandSize = 32 (* quadword/doubleword operation *)
                    THEN
                        temp  =  EDX:EAX / SRC;
                        IF temp > FFFFFFFFH
                            THEN #DE; (* divide error *) ;
                        ELSE
                            EAX  =  temp;
                            EDX  =  EDX:EAX MOD SRC;
                        FI;
                    FI;
                ELSE IF OperandSize = 64 (*Doublequadword/quadword operation*)
                    THEN
                        temp = RDX:RAX / SRC;
                        IF temp > FFFFFFFFFFFFFFFFH
                            THEN #DE; (* Divide error *)
                        ELSE
                            RAX = temp;
                            RDX = RDX:RAX MOD SRC;
                        FI;
                    FI;
            FI;

        :param cpu: current CPU.
        :param src: source operand.
        """
        size = src.size
        reg_name_h = {8: 'DL', 16: 'DX', 32: 'EDX', 64: 'RDX'}[size]
        reg_name_l = {8: 'AL', 16: 'AX', 32: 'EAX', 64: 'RAX'}[size]

        dividend = Operators.CONCAT(size * 2,
                                    cpu.read_register(reg_name_h),
                                    cpu.read_register(reg_name_l))
        divisor = Operators.ZEXTEND(src.read(), size * 2)

        # TODO make symbol friendly
        if isinstance(divisor, int) and divisor == 0:
            raise DivideByZeroError()
        quotient = Operators.UDIV(dividend, divisor)

        MASK = (1 << size) - 1

        # TODO make symbol friendly
        if isinstance(quotient, int) and quotient > MASK:
            raise DivideByZeroError()
        remainder = Operators.UREM(dividend, divisor)

        cpu.write_register(reg_name_l, Operators.EXTRACT(quotient, 0, size))
        cpu.write_register(reg_name_h, Operators.EXTRACT(remainder, 0, size))