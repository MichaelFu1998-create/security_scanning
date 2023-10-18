def MUL(cpu, src):
        """
        Unsigned multiply.

        Performs an unsigned multiplication of the first operand (destination
        operand) and the second operand (source operand) and stores the result
        in the destination operand. The destination operand is an implied operand
        located in register AL, AX or EAX (depending on the size of the operand);
        the source operand is located in a general-purpose register or a memory location.

        The result is stored in register AX, register pair DX:AX, or register
        pair EDX:EAX (depending on the operand size), with the high-order bits
        of the product contained in register AH, DX, or EDX, respectively. If
        the high-order bits of the product are 0, the CF and OF flags are cleared;
        otherwise, the flags are set::

                IF byte operation
                THEN
                    AX  =  AL * SRC
                ELSE (* word or doubleword operation *)
                    IF OperandSize  =  16
                    THEN
                        DX:AX  =  AX * SRC
                    ELSE (* OperandSize  =  32 *)
                        EDX:EAX  =  EAX * SRC
                    FI;
                FI;

        :param cpu: current CPU.
        :param src: source operand.
        """
        size = src.size
        reg_name_low, reg_name_high = {8: ('AL', 'AH'),
                                       16: ('AX', 'DX'),
                                       32: ('EAX', 'EDX'),
                                       64: ('RAX', 'RDX')}[size]
        res = (Operators.ZEXTEND(cpu.read_register(reg_name_low), 256) *
               Operators.ZEXTEND(src.read(), 256))
        cpu.write_register(reg_name_low, Operators.EXTRACT(res, 0, size))
        cpu.write_register(reg_name_high, Operators.EXTRACT(res, size, size))
        cpu.OF = Operators.EXTRACT(res, size, size) != 0
        cpu.CF = cpu.OF