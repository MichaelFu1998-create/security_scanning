def IMUL(cpu, *operands):
        """
        Signed multiply.

        Performs a signed multiplication of two operands. This instruction has
        three forms, depending on the number of operands.
            - One-operand form. This form is identical to that used by the MUL
            instruction. Here, the source operand (in a general-purpose
            register or memory location) is multiplied by the value in the AL,
            AX, or EAX register (depending on the operand size) and the product
            is stored in the AX, DX:AX, or EDX:EAX registers, respectively.
            - Two-operand form. With this form the destination operand (the
            first operand) is multiplied by the source operand (second
            operand). The destination operand is a general-purpose register and
            the source operand is an immediate value, a general-purpose
            register, or a memory location. The product is then stored in the
            destination operand location.
            - Three-operand form. This form requires a destination operand (the
            first operand) and two source operands (the second and the third
            operands). Here, the first source operand (which can be a
            general-purpose register or a memory location) is multiplied by the
            second source operand (an immediate value). The product is then
            stored in the destination operand (a general-purpose register).

        When an immediate value is used as an operand, it is sign-extended to
        the length of the destination operand format. The CF and OF flags are
        set when significant bits are carried into the upper half of the
        result. The CF and OF flags are cleared when the result fits exactly in
        the lower half of the result. The three forms of the IMUL instruction
        are similar in that the length of the product is calculated to twice
        the length of the operands. With the one-operand form, the product is
        stored exactly in the destination. With the two- and three- operand
        forms, however, result is truncated to the length of the destination
        before it is stored in the destination register. Because of this
        truncation, the CF or OF flag should be tested to ensure that no
        significant bits are lost. The two- and three-operand forms may also be
        used with unsigned operands because the lower half of the product is
        the same regardless if the operands are signed or unsigned. The CF and
        OF flags, however, cannot be used to determine if the upper half of the
        result is non-zero::

        IF (NumberOfOperands == 1)
        THEN
            IF (OperandSize == 8)
            THEN
                AX = AL * SRC (* Signed multiplication *)
                IF AL == AX
                THEN
                    CF = 0; OF = 0;
                ELSE
                    CF = 1; OF = 1;
                FI;
            ELSE
                IF OperandSize == 16
                THEN
                    DX:AX = AX * SRC (* Signed multiplication *)
                    IF sign_extend_to_32 (AX) == DX:AX
                    THEN
                        CF = 0; OF = 0;
                    ELSE
                        CF = 1; OF = 1;
                    FI;
                ELSE
                    IF OperandSize == 32
                    THEN
                        EDX:EAX = EAX * SRC (* Signed multiplication *)
                        IF EAX == EDX:EAX
                        THEN
                            CF = 0; OF = 0;
                        ELSE
                            CF = 1; OF = 1;
                        FI;
                    ELSE (* OperandSize = 64 *)
                        RDX:RAX = RAX * SRC (* Signed multiplication *)
                        IF RAX == RDX:RAX
                        THEN
                            CF = 0; OF = 0;
                        ELSE
                           CF = 1; OF = 1;
                        FI;
                    FI;
                FI;
        ELSE
            IF (NumberOfOperands = 2)
            THEN
                temp = DEST * SRC (* Signed multiplication; temp is double DEST size *)
                DEST = DEST * SRC (* Signed multiplication *)
                IF temp != DEST
                THEN
                    CF = 1; OF = 1;
                ELSE
                    CF = 0; OF = 0;
                FI;
            ELSE (* NumberOfOperands = 3 *)
                DEST = SRC1 * SRC2 (* Signed multiplication *)
                temp = SRC1 * SRC2 (* Signed multiplication; temp is double SRC1 size *)
                IF temp != DEST
                THEN
                    CF = 1; OF = 1;
                ELSE
                    CF = 0; OF = 0;
                FI;
            FI;
        FI;

        :param cpu: current CPU.
        :param operands: variable list of operands.
        """
        dest = operands[0]
        OperandSize = dest.size
        reg_name_h = {8: 'AH', 16: 'DX', 32: 'EDX', 64: 'RDX'}[OperandSize]
        reg_name_l = {8: 'AL', 16: 'AX', 32: 'EAX', 64: 'RAX'}[OperandSize]

        arg0 = dest.read()
        arg1 = None
        arg2 = None
        res = None
        if len(operands) == 1:
            arg1 = cpu.read_register(reg_name_l)
            temp = (Operators.SEXTEND(arg0, OperandSize, OperandSize * 2) *
                    Operators.SEXTEND(arg1, OperandSize, OperandSize * 2))
            temp = temp & ((1 << (OperandSize * 2)) - 1)
            cpu.write_register(reg_name_l,
                               Operators.EXTRACT(temp, 0, OperandSize))
            cpu.write_register(reg_name_h,
                               Operators.EXTRACT(temp, OperandSize, OperandSize))
            res = Operators.EXTRACT(temp, 0, OperandSize)
        elif len(operands) == 2:
            arg1 = operands[1].read()
            arg1 = Operators.SEXTEND(arg1, OperandSize, OperandSize * 2)
            temp = Operators.SEXTEND(arg0, OperandSize, OperandSize * 2) * arg1
            temp = temp & ((1 << (OperandSize * 2)) - 1)
            res = dest.write(Operators.EXTRACT(temp, 0, OperandSize))
        else:
            arg1 = operands[1].read()
            arg2 = operands[2].read()
            temp = (Operators.SEXTEND(arg1, OperandSize, OperandSize * 2) *
                    Operators.SEXTEND(arg2, operands[2].size, OperandSize * 2))
            temp = temp & ((1 << (OperandSize * 2)) - 1)
            res = dest.write(Operators.EXTRACT(temp, 0, OperandSize))

        cpu.CF = (Operators.SEXTEND(res, OperandSize, OperandSize * 2) != temp)
        cpu.OF = cpu.CF