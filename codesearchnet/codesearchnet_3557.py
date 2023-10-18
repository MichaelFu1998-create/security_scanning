def visit_BitVecOr(self, expression, *operands):
        """ a | 0 => a
            0 | a => a
            0xffffffff & a => 0xffffffff
            a & 0xffffffff => 0xffffffff

        """
        left = expression.operands[0]
        right = expression.operands[1]
        if isinstance(right, BitVecConstant):
            if right.value == 0:
                return left
            elif right.value == left.mask:
                return right
            elif isinstance(left, BitVecOr):
                left_left = left.operands[0]
                left_right = left.operands[1]
                if isinstance(right, Constant):
                    return BitVecOr(left_left, (left_right | right), taint=expression.taint)
        elif isinstance(left, BitVecConstant):
            return BitVecOr(right, left, taint=expression.taint)