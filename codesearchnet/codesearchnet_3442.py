def _hook_syscall(self, uc, data):
        """
        Unicorn hook that transfers control to Manticore so it can execute the syscall
        """
        logger.debug(f"Stopping emulation at {hex(uc.reg_read(self._to_unicorn_id('RIP')))} to perform syscall")
        self.sync_unicorn_to_manticore()
        from ..native.cpu.abstractcpu import Syscall
        self._to_raise = Syscall()
        uc.emu_stop()