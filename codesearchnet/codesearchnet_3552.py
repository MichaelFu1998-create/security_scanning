def visit_Operation(self, expression, *operands):
        """ constant folding, if all operands of an expression are a Constant do the math """
        if all(isinstance(o, Constant) for o in operands):
            expression = constant_folder(expression)
        if self._changed(expression, operands):
            expression = self._rebuild(expression, operands)
        return expression