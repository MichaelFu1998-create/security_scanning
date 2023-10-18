def instruction(self):
        """
        Current instruction pointed by self.pc
        """
        # FIXME check if pc points to invalid instruction
        # if self.pc >= len(self.bytecode):
        #    return InvalidOpcode('Code out of range')
        # if self.pc in self.invalid:
        #    raise InvalidOpcode('Opcode inside a PUSH immediate')
        try:
            _decoding_cache = getattr(self, '_decoding_cache')
        except Exception:
            _decoding_cache = self._decoding_cache = {}

        pc = self.pc
        if isinstance(pc, Constant):
            pc = pc.value

        if pc in _decoding_cache:
            return _decoding_cache[pc]

        def getcode():
            bytecode = self.bytecode
            for pc_i in range(pc, len(bytecode)):
                yield simplify(bytecode[pc_i]).value
            while True:
                yield 0
        instruction = EVMAsm.disassemble_one(getcode(), pc=pc, fork=DEFAULT_FORK)
        _decoding_cache[pc] = instruction
        return instruction