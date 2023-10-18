def MRC(cpu, coprocessor, opcode1, dest, coprocessor_reg_n, coprocessor_reg_m, opcode2):
        """
        MRC moves to ARM register from coprocessor.

        :param Armv7Operand coprocessor: The name of the coprocessor; immediate
        :param Armv7Operand opcode1: coprocessor specific opcode; 3-bit immediate
        :param Armv7Operand dest: the destination operand: register
        :param Armv7Operand coprocessor_reg_n: the coprocessor register; immediate
        :param Armv7Operand coprocessor_reg_m: the coprocessor register; immediate
        :param Armv7Operand opcode2: coprocessor specific opcode; 3-bit immediate
        """
        assert coprocessor.type == 'coprocessor'
        assert opcode1.type == 'immediate'
        assert opcode2.type == 'immediate'
        assert dest.type == 'register'
        imm_coprocessor = coprocessor.read()
        imm_opcode1 = opcode1.read()
        imm_opcode2 = opcode2.read()
        coprocessor_n_name = coprocessor_reg_n.read()
        coprocessor_m_name = coprocessor_reg_m.read()

        if 15 == imm_coprocessor:  # MMU
            if 0 == imm_opcode1:
                if 13 == coprocessor_n_name:
                    if 3 == imm_opcode2:
                        dest.write(cpu.regfile.read('P15_C13'))
                        return
        raise NotImplementedError("MRC: unimplemented combination of coprocessor, opcode, and coprocessor register")