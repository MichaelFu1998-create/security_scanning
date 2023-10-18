def IDIV(cpu, src):
        """
        Signed divide.

        Divides (signed) the value in the AL, AX, or EAX register by the source
        operand and stores the result in the AX, DX:AX, or EDX:EAX registers.
        The source operand can be a general-purpose register or a memory
        location. The action of this instruction depends on the operand size.::

        IF SRC  =  0
        THEN #DE; (* divide error *)
        FI;
        IF OpernadSize  =  8 (* word/byte operation *)
        THEN
            temp  =  AX / SRC; (* signed division *)
            IF (temp > 7FH) Operators.OR(temp < 80H)
            (* if a positive result is greater than 7FH or a negative result is
            less than 80H *)
            THEN #DE; (* divide error *) ;
            ELSE
                AL  =  temp;
                AH  =  AX SignedModulus SRC;
            FI;
        ELSE
            IF OpernadSize  =  16 (* doubleword/word operation *)
            THEN
                temp  =  DX:AX / SRC; (* signed division *)
                IF (temp > 7FFFH) Operators.OR(temp < 8000H)
                (* if a positive result is greater than 7FFFH *)
                (* or a negative result is less than 8000H *)
                THEN #DE; (* divide error *) ;
                ELSE
                    AX  =  temp;
                    DX  =  DX:AX SignedModulus SRC;
                FI;
            ELSE (* quadword/doubleword operation *)
                temp  =  EDX:EAX / SRC; (* signed division *)
                IF (temp > 7FFFFFFFH) Operators.OR(temp < 80000000H)
                (* if a positive result is greater than 7FFFFFFFH *)
                (* or a negative result is less than 80000000H *)
                THEN #DE; (* divide error *) ;
                ELSE
                    EAX  =  temp;
                    EDX  =  EDX:EAX SignedModulus SRC;
                FI;
            FI;
        FI;

        :param cpu: current CPU.
        :param src: source operand.
        """

        reg_name_h = {8: 'AH', 16: 'DX', 32: 'EDX', 64: 'RDX'}[src.size]
        reg_name_l = {8: 'AL', 16: 'AX', 32: 'EAX', 64: 'RAX'}[src.size]

        dividend = Operators.CONCAT(src.size * 2,
                                    cpu.read_register(reg_name_h),
                                    cpu.read_register(reg_name_l))

        divisor = src.read()
        if isinstance(divisor, int) and divisor == 0:
            raise DivideByZeroError()

        dst_size = src.size * 2

        divisor = Operators.SEXTEND(divisor, src.size, dst_size)
        mask = (1 << dst_size) - 1
        sign_mask = 1 << (dst_size - 1)

        dividend_sign = (dividend & sign_mask) != 0
        divisor_sign = (divisor & sign_mask) != 0

        if isinstance(divisor, int):
            if divisor_sign:
                divisor = ((~divisor) + 1) & mask
                divisor = -divisor

        if isinstance(dividend, int):
            if dividend_sign:
                dividend = ((~dividend) + 1) & mask
                dividend = -dividend

        quotient = Operators.SDIV(dividend, divisor)
        if (isinstance(dividend, int) and
                isinstance(dividend, int)):
            # handle the concrete case
            remainder = dividend - (quotient * divisor)
        else:
            # symbolic case -- optimize via SREM
            remainder = Operators.SREM(dividend, divisor)

        cpu.write_register(reg_name_l, Operators.EXTRACT(quotient, 0, src.size))
        cpu.write_register(reg_name_h, Operators.EXTRACT(remainder, 0, src.size))