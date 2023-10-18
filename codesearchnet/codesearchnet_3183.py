def _get_flags(self, reg):
        """ Build EFLAGS/RFLAGS from flags """
        def make_symbolic(flag_expr):
            register_size = 32 if reg == 'EFLAGS' else 64
            value, offset = flag_expr
            return Operators.ITEBV(register_size, value,
                                   BitVecConstant(register_size, 1 << offset),
                                   BitVecConstant(register_size, 0))

        flags = []
        for flag, offset in self._flags.items():
            flags.append((self._registers[flag], offset))

        if any(issymbolic(flag) for flag, offset in flags):
            res = reduce(operator.or_, map(make_symbolic, flags))
        else:
            res = 0
            for flag, offset in flags:
                res += flag << offset
        return res