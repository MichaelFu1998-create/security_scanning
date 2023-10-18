def _step(self, instruction, chunksize=0):
        """
        Execute a chunk fo instructions starting from instruction
        :param instruction: Where to start
        :param chunksize: max number of instructions to execute. Defaults to infinite.
        """

        try:
            pc = self._cpu.PC
            m = self._cpu.memory.map_containing(pc)
            if self._stop_at:
                logger.info(f"Emulating from {hex(pc)} to  {hex(self._stop_at)}")
            self._emu.emu_start(pc, m.end if not self._stop_at else self._stop_at, count=chunksize)
        except UcError:
            # We request re-execution by signaling error; if we we didn't set
            # _should_try_again, it was likely an actual error
            if not self._should_try_again:
                raise

        if self._should_try_again:
            return

        # self.sync_unicorn_to_manticore()
        self._cpu.PC = self.get_unicorn_pc()
        if self._cpu.PC == self._stop_at:
            logger.info("Reached emulation target, switching to Manticore mode")
            self.sync_unicorn_to_manticore()
            self._stop_at = None

        # Raise the exception from a hook that Unicorn would have eaten
        if self._to_raise:
            from ..native.cpu.abstractcpu import Syscall
            if type(self._to_raise) is not Syscall:
                logger.info("Raising %s", self._to_raise)
            raise self._to_raise

        logger.info(f"Exiting Unicorn Mode at {hex(self._cpu.PC)}")
        return