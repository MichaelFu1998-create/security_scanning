def _set_flags(self, reg, res):
        """ Set individual flags from a EFLAGS/RFLAGS value """
        #assert sizeof (res) == 32 if reg == 'EFLAGS' else 64
        for flag, offset in self._flags.items():
            self.write(flag, Operators.EXTRACT(res, offset, 1))