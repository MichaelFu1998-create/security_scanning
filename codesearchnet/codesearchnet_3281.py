def LOOP(cpu, dest):
        """
        Loops according to ECX counter.

        Performs a loop operation using the ECX or CX register as a counter.
        Each time the LOOP instruction is executed, the count register is decremented,
        then checked for 0. If the count is 0, the loop is terminated and program
        execution continues with the instruction following the LOOP instruction.
        If the count is not zero, a near jump is performed to the destination
        (target) operand, which is presumably the instruction at the beginning
        of the loop. If the address-size attribute is 32 bits, the ECX register
        is used as the count register; otherwise the CX register is used::

                IF address_bit_size  =  32
                THEN
                    Count is ECX;
                ELSE (* address_bit_size  =  16 *)
                    Count is CX;
                FI;
                Count  =  Count - 1;

                IF (Count  0)  =  1
                THEN
                    EIP  =  EIP + SignExtend(DEST);
                    IF OperandSize  =  16
                    THEN
                        EIP  =  EIP AND 0000FFFFH;
                    FI;
                ELSE
                    Terminate loop and continue program execution at EIP;
                FI;

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        counter_name = {16: 'CX', 32: 'ECX', 64: 'RCX'}[cpu.address_bit_size]
        counter = cpu.write_register(counter_name, cpu.read_register(counter_name) - 1)
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, counter == 0, (cpu.PC + dest.read()) & ((1 << dest.size) - 1), cpu.PC + cpu.instruction.size)