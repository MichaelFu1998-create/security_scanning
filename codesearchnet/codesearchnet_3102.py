def lr(self, lis, op):
        """performs this operation on a list from *left to right*
        op must take 2 args
        a,b,c  => op(op(a, b), c)"""
        it = iter(lis)
        res = trans(it.next())
        for e in it:
            e = trans(e)
            res = op(res, e)
        return res