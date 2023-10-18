def visit_BitVecAdd(self, expression, *operands):
        """ a + 0  ==> a
            0 + a  ==> a
        """
        left = expression.operands[0]
        right = expression.operands[1]
        if isinstance(right, BitVecConstant):
            if right.value == 0:
                return left
        if isinstance(left, BitVecConstant):
            if left.value == 0:
                return right