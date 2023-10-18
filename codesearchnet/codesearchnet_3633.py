def STREX(cpu, status, *args):
        """
        STREX performs a conditional store to memory.
        :param Armv7Operand status: the destination register for the returned status; register
        """
        # TODO: implement conditional return with appropriate status --GR, 2017-06-06
        status.write(0)
        return cpu._STR(cpu.address_bit_size, *args)