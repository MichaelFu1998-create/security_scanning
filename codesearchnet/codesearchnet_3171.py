def decode_instruction(self, pc):
        """
        This will decode an instruction from memory pointed by `pc`

        :param int pc: address of the instruction
        """
        # No dynamic code!!! #TODO!
        # Check if instruction was already decoded
        if pc in self._instruction_cache:
            return self._instruction_cache[pc]

        text = b''

        # Read Instruction from memory
        for address in range(pc, pc + self.max_instr_width):
            # This reads a byte from memory ignoring permissions
            # and concretize it if symbolic
            if not self.memory.access_ok(address, 'x'):
                break

            c = self.memory[address]

            if issymbolic(c):
                # In case of fully symbolic memory, eagerly get a valid ptr
                if isinstance(self.memory, LazySMemory):
                    try:
                        vals = visitors.simplify_array_select(c)
                        c = bytes([vals[0]])
                    except visitors.ArraySelectSimplifier.ExpressionNotSimple:
                        c = struct.pack('B', solver.get_value(self.memory.constraints, c))
                elif isinstance(c, Constant):
                    c = bytes([c.value])
                else:
                    logger.error('Concretize executable memory %r %r', c, text)
                    raise ConcretizeMemory(self.memory,
                                           address=pc,
                                           size=8 * self.max_instr_width,
                                           policy='INSTRUCTION')
            text += c

        # Pad potentially incomplete instruction with zeroes
        code = text.ljust(self.max_instr_width, b'\x00')

        try:
            # decode the instruction from code
            insn = self.disasm.disassemble_instruction(code, pc)
        except StopIteration as e:
            raise DecodeException(pc, code)

        # Check that the decoded instruction is contained in executable memory
        if not self.memory.access_ok(slice(pc, pc + insn.size), 'x'):
            logger.info("Trying to execute instructions from non-executable memory")
            raise InvalidMemoryAccess(pc, 'x')

        insn.operands = self._wrap_operands(insn.operands)
        self._instruction_cache[pc] = insn
        return insn