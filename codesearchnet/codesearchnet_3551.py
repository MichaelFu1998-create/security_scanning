def visit_Operation(self, expression, *operands):
        """ constant folding, if all operands of an expression are a Constant do the math """
        operation = self.operations.get(type(expression), None)
        if operation is not None and \
                all(isinstance(o, Constant) for o in operands):
            value = operation(*(x.value for x in operands))
            if isinstance(expression, BitVec):
                return BitVecConstant(expression.size, value, taint=expression.taint)
            else:
                isinstance(expression, Bool)
                return BoolConstant(value, taint=expression.taint)
        else:
            if any(operands[i] is not expression.operands[i] for i in range(len(operands))):
                expression = self._rebuild(expression, operands)
        return expression