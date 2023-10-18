def ADDMOD(self, a, b, c):
        """Modulo addition operation"""
        try:
            result = Operators.ITEBV(256, c == 0, 0, (a + b) % c)
        except ZeroDivisionError:
            result = 0
        return result