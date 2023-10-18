def GT(self, a, b):
        """Greater-than comparison"""
        return Operators.ITEBV(256, Operators.UGT(a, b), 1, 0)