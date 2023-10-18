def LOOPNZ(cpu, target):
        """
        Loops if ECX counter is nonzero.

        :param cpu: current CPU.
        :param target: destination operand.
        """
        counter_name = {16: 'CX', 32: 'ECX', 64: 'RCX'}[cpu.address_bit_size]
        counter = cpu.write_register(counter_name, cpu.read_register(counter_name) - 1)
        cpu.PC = Operators.ITEBV(cpu.address_bit_size, counter != 0, (cpu.PC + target.read()) & ((1 << target.size) - 1), cpu.PC + cpu.instruction.size)