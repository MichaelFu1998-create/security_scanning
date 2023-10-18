def emulate(self, insn):
        """
        Pick the right emulate function (maintains API compatiblity)

        :param insn: single instruction to emulate/start emulation from
        """

        if self._concrete:
            self.concrete_emulate(insn)
        else:
            self.backup_emulate(insn)