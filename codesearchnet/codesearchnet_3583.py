def MOD(self, a, b):
        """Modulo remainder operation"""
        try:
            result = Operators.ITEBV(256, b == 0, 0, a % b)
        except ZeroDivisionError:
            result = 0
        return result