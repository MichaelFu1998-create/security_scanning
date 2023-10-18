def CMPXCHG8B(cpu, dest):
        """
        Compares and exchanges bytes.

        Compares the 64-bit value in EDX:EAX (or 128-bit value in RDX:RAX if
        operand size is 128 bits) with the operand (destination operand). If
        the values are equal, the 64-bit value in ECX:EBX (or 128-bit value in
        RCX:RBX) is stored in the destination operand.  Otherwise, the value in
        the destination operand is loaded into EDX:EAX (or RDX:RAX)::

                IF (64-Bit Mode and OperandSize = 64)
                THEN
                    IF (RDX:RAX = DEST)
                    THEN
                        ZF = 1;
                        DEST = RCX:RBX;
                    ELSE
                        ZF = 0;
                        RDX:RAX = DEST;
                    FI
                ELSE
                    IF (EDX:EAX = DEST)
                    THEN
                        ZF = 1;
                        DEST = ECX:EBX;
                    ELSE
                        ZF = 0;
                        EDX:EAX = DEST;
                    FI;
                FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        size = dest.size
        cmp_reg_name_l = {64: 'EAX', 128: 'RAX'}[size]
        cmp_reg_name_h = {64: 'EDX', 128: 'RDX'}[size]
        src_reg_name_l = {64: 'EBX', 128: 'RBX'}[size]
        src_reg_name_h = {64: 'ECX', 128: 'RCX'}[size]

        # EDX:EAX or RDX:RAX
        cmph = cpu.read_register(cmp_reg_name_h)
        cmpl = cpu.read_register(cmp_reg_name_l)

        srch = cpu.read_register(src_reg_name_h)
        srcl = cpu.read_register(src_reg_name_l)

        cmp0 = Operators.CONCAT(size, cmph, cmpl)
        src0 = Operators.CONCAT(size, srch, srcl)
        arg_dest = dest.read()
        cpu.ZF = arg_dest == cmp0

        dest.write(
            Operators.ITEBV(size, cpu.ZF,
                            Operators.CONCAT(size, srch, srcl),
                            arg_dest)
        )
        cpu.write_register(cmp_reg_name_l, Operators.ITEBV(size // 2, cpu.ZF, cmpl,
                                                           Operators.EXTRACT(arg_dest, 0, size // 2)))
        cpu.write_register(cmp_reg_name_h, Operators.ITEBV(size // 2, cpu.ZF, cmph,
                                                           Operators.EXTRACT(arg_dest, size // 2, size // 2)))