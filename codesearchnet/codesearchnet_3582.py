def SDIV(self, a, b):
        """Signed integer division operation (truncated)"""
        s0, s1 = to_signed(a), to_signed(b)
        try:
            result = (Operators.ABS(s0) // Operators.ABS(s1) * Operators.ITEBV(256, (s0 < 0) != (s1 < 0), -1, 1))
        except ZeroDivisionError:
            result = 0
        result = Operators.ITEBV(256, b == 0, 0, result)
        if not issymbolic(result):
            result = to_signed(result)
        return result