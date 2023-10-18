def SWAP(self, *operands):
        """Exchange 1st and 2nd stack items"""
        a = operands[0]
        b = operands[-1]
        return (b,) + operands[1:-1] + (a,)