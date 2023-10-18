def TBH(cpu, dest):
        """
        Table Branch Halfword causes a PC-relative forward branch using a table of single halfword offsets. A base
        register provides a pointer to the table, and a second register supplies an index into the table. The branch
        length is twice the value of the halfword returned from the table.

        :param ARMv7Operand dest: see below; register
        """
        # Capstone merges the two registers values into one operand, so we need to extract them back

        # Specifies the base register. This contains the address of the table of branch lengths. This
        # register is allowed to be the PC. If it is, the table immediately follows this instruction.
        base_addr = dest.get_mem_base_addr()
        if dest.mem.base in ('PC', 'R15'):
            base_addr = cpu.PC

        # Specifies the index register. This contains an integer pointing to a halfword within the table.
        # The offset within the table is twice the value of the index.
        offset = cpu.read_int(base_addr + dest.get_mem_offset(), 16)
        offset = Operators.ZEXTEND(offset, cpu.address_bit_size)

        cpu.PC += (offset << 1)