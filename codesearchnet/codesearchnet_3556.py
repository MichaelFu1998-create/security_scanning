def visit_BitVecSub(self, expression, *operands):
        """ a - 0 ==> 0
            (a + b) - b  ==> a
            (b + a) - b  ==> a
        """
        left = expression.operands[0]
        right = expression.operands[1]
        if isinstance(left, BitVecAdd):
            if self._same_constant(left.operands[0], right):
                return left.operands[1]
            elif self._same_constant(left.operands[1], right):
                return left.operands[0]