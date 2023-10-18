def CMPS(cpu, dest, src):
        """
        Compares string operands.

        Compares the byte, word, double word or quad specified with the first source
        operand with the byte, word, double or quad word specified with the second
        source operand and sets the status flags in the EFLAGS register according
        to the results. Both the source operands are located in memory::

                temp  = SRC1 - SRC2;
                SetStatusFlags(temp);
                IF (byte comparison)
                THEN IF DF  =  0
                    THEN
                        (E)SI  =  (E)SI + 1;
                        (E)DI  =  (E)DI + 1;
                    ELSE
                        (E)SI  =  (E)SI - 1;
                        (E)DI  =  (E)DI - 1;
                    FI;
                ELSE IF (word comparison)
                    THEN IF DF  =  0
                        (E)SI  =  (E)SI + 2;
                        (E)DI  =  (E)DI + 2;
                    ELSE
                        (E)SI  =  (E)SI - 2;
                        (E)DI  =  (E)DI - 2;
                    FI;
                ELSE (* doubleword comparison*)
                    THEN IF DF  =  0
                        (E)SI  =  (E)SI + 4;
                        (E)DI  =  (E)DI + 4;
                    ELSE
                        (E)SI  =  (E)SI - 4;
                        (E)DI  =  (E)DI - 4;
                    FI;
                FI;

        :param cpu: current CPU.
        :param dest: first source operand.
        :param src: second source operand.
        """
        src_reg = {8: 'SI', 32: 'ESI', 64: 'RSI'}[cpu.address_bit_size]
        dest_reg = {8: 'DI', 32: 'EDI', 64: 'RDI'}[cpu.address_bit_size]

        base, _, ty = cpu.get_descriptor(cpu.DS)

        src_addr = cpu.read_register(src_reg) + base
        dest_addr = cpu.read_register(dest_reg) + base
        size = dest.size

        # Compare
        arg1 = cpu.read_int(dest_addr, size)
        arg0 = cpu.read_int(src_addr, size)
        res = (arg0 - arg1) & ((1 << size) - 1)

        cpu._calculate_CMP_flags(size, res, arg0, arg1)

        #Advance EDI/ESI pointers
        increment = Operators.ITEBV(cpu.address_bit_size, cpu.DF, -size // 8, size // 8)
        cpu.write_register(src_reg, cpu.read_register(src_reg) + increment)
        cpu.write_register(dest_reg, cpu.read_register(dest_reg) + increment)