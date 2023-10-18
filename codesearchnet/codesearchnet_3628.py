def MOVT(cpu, dest, src):
        """
        MOVT writes imm16 to Rd[31:16]. The write does not affect Rd[15:0].

        :param Armv7Operand dest: The destination operand; register
        :param Armv7Operand src: The source operand; 16-bit immediate
        """
        assert src.type == 'immediate'
        imm = src.read()
        low_halfword = dest.read() & Mask(16)
        dest.write((imm << 16) | low_halfword)