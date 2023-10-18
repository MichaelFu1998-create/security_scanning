def visit_BitVecShiftLeft(self, expression, *operands):
        """ a << 0 => a                       remove zero
            a << ct => 0 if ct > sizeof(a)    remove big constant shift
        """
        left = expression.operands[0]
        right = expression.operands[1]
        if isinstance(right, BitVecConstant):
            if right.value == 0:
                return left
            elif right.value >= right.size:
                return left