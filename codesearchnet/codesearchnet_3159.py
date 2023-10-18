def emulate_until(self, target: int):
        """
        Tells the CPU to set up a concrete unicorn emulator and use it to execute instructions
        until target is reached.

        :param target: Where Unicorn should hand control back to Manticore. Set to 0 for all instructions.
        """
        self._concrete = True
        self._break_unicorn_at = target
        if self.emu:
            self.emu._stop_at = target