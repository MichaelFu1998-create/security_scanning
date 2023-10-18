def visit_BitVecAnd(self, expression, *operands):
        """ ct & x => x & ct                move constants to the right
            a & 0 => 0                      remove zero
            a & 0xffffffff => a             remove full mask
            (b & ct2) & ct => b & (ct&ct2)  associative property
            (a & (b | c) => a&b | a&c       distribute over |
        """
        left = expression.operands[0]
        right = expression.operands[1]
        if isinstance(right, BitVecConstant):
            if right.value == 0:
                return right
            elif right.value == right.mask:
                return left
            elif isinstance(left, BitVecAnd):
                left_left = left.operands[0]
                left_right = left.operands[1]
                if isinstance(right, Constant):
                    return BitVecAnd(left_left, left_right & right, taint=expression.taint)
            elif isinstance(left, BitVecOr):
                left_left = left.operands[0]
                left_right = left.operands[1]
                return BitVecOr(right & left_left, right & left_right, taint=expression.taint)

        elif isinstance(left, BitVecConstant):
            return BitVecAnd(right, left, taint=expression.taint)