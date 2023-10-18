def PUSH(cpu, src):
        """
        Pushes a value onto the stack.

        Decrements the stack pointer and then stores the source operand on the top of the stack.

        :param cpu: current CPU.
        :param src: source operand.
        """
        # http://stackoverflow.com/questions/11291151/how-push-imm-encodes
        size = src.size
        v = src.read()
        if size != 64 and size != cpu.address_bit_size // 2:
            v = Operators.SEXTEND(v, size, cpu.address_bit_size)
            size = cpu.address_bit_size
        cpu.push(v, size)