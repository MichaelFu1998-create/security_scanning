def rl(self, lis, op):
        """performs this operation on a list from *right to left*
        op must take 2 args
        a,b,c  => op(a, op(b, c))"""
        it = reversed(lis)
        res = trans(it.next())
        for e in it:
            e = trans(e)
            res = op(e, res)
        return res