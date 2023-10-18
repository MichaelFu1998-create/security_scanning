def SCAS(cpu, dest, src):
        """
        Scans String.

        Compares the byte, word, or double word specified with the memory operand
        with the value in the AL, AX, EAX, or RAX register, and sets the status flags
        according to the results. The memory operand address is read from either
        the ES:RDI, ES:EDI or the ES:DI registers (depending on the address-size
        attribute of the instruction, 32 or 16, respectively)::

                IF (byte comparison)
                THEN
                    temp  =  AL - SRC;
                    SetStatusFlags(temp);
                    THEN IF DF  =  0
                        THEN (E)DI  =  (E)DI + 1;
                        ELSE (E)DI  =  (E)DI - 1;
                        FI;
                    ELSE IF (word comparison)
                        THEN
                            temp  =  AX - SRC;
                            SetStatusFlags(temp)
                            THEN IF DF  =  0
                                THEN (E)DI  =  (E)DI + 2;
                                ELSE (E)DI  =  (E)DI - 2;
                                FI;
                     ELSE (* doubleword comparison *)
                           temp  =  EAX - SRC;
                           SetStatusFlags(temp)
                           THEN IF DF  =  0
                                THEN
                                    (E)DI  =  (E)DI + 4;
                                ELSE
                                    (E)DI  =  (E)DI - 4;
                                FI;
                           FI;
                     FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        dest_reg = dest.reg
        mem_reg = src.mem.base  # , src.type, src.read()
        size = dest.size
        arg0 = dest.read()
        arg1 = src.read()
        res = arg0 - arg1
        cpu._calculate_CMP_flags(size, res, arg0, arg1)

        increment = Operators.ITEBV(cpu.address_bit_size, cpu.DF, -size // 8, size // 8)
        cpu.write_register(mem_reg, cpu.read_register(mem_reg) + increment)