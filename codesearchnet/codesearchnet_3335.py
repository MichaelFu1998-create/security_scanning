def XLATB(cpu):
        """
        Table look-up translation.

        Locates a byte entry in a table in memory, using the contents of the
        AL register as a table index, then copies the contents of the table entry
        back into the AL register. The index in the AL register is treated as
        an unsigned integer. The XLAT and XLATB instructions get the base address
        of the table in memory from either the DS:EBX or the DS:BX registers.
        In 64-bit mode, operation is similar to that in legacy or compatibility mode.
        AL is used to specify the table index (the operand size is fixed at 8 bits).
        RBX, however, is used to specify the table's base address::

                IF address_bit_size = 16
                THEN
                    AL = (DS:BX + ZeroExtend(AL));
                ELSE IF (address_bit_size = 32)
                    AL = (DS:EBX + ZeroExtend(AL)); FI;
                ELSE (address_bit_size = 64)
                    AL = (RBX + ZeroExtend(AL));
                FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        cpu.AL = cpu.read_int(cpu.EBX + Operators.ZEXTEND(cpu.AL, 32), 8)