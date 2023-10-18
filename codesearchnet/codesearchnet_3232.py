def SAHF(cpu):
        """
        Stores AH into flags.

        Loads the SF, ZF, AF, PF, and CF flags of the EFLAGS register with values
        from the corresponding bits in the AH register (bits 7, 6, 4, 2, and 0,
        respectively). Bits 1, 3, and 5 of register AH are ignored; the corresponding
        reserved bits (1, 3, and 5) in the EFLAGS register remain as shown below::

                EFLAGS(SF:ZF:0:AF:0:PF:1:CF)  =  AH;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """

        eflags_size = 32
        val = cpu.AH & 0xD5 | 0x02

        cpu.EFLAGS = Operators.ZEXTEND(val, eflags_size)