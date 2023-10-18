def LT(self, a, b):
        """Less-than comparison"""
        return Operators.ITEBV(256, Operators.ULT(a, b), 1, 0)