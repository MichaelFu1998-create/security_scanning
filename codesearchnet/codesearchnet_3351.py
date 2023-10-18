def emulate(self, instruction):
        """
        Emulate a single instruction.
        """

        # The emulation might restart if Unicorn needs to bring in a memory map
        # or bring a value from Manticore state.
        while True:

            self.reset()

            # Establish Manticore state, potentially from past emulation
            # attempts
            for base in self._should_be_mapped:
                size, perms = self._should_be_mapped[base]
                self._emu.mem_map(base, size, perms)

            for address, values in self._should_be_written.items():
                for offset, byte in enumerate(values, start=address):
                    if issymbolic(byte):
                        from ..native.cpu.abstractcpu import ConcretizeMemory
                        raise ConcretizeMemory(self._cpu.memory, offset, 8,
                                               "Concretizing for emulation")

                self._emu.mem_write(address, b''.join(values))

            # Try emulation
            self._should_try_again = False

            self._step(instruction)

            if not self._should_try_again:
                break