def visit_ArraySelect(self, expression, *operands):
        """ ArraySelect (ArrayStore((ArrayStore(x0,v0) ...),xn, vn), x0)
                -> v0
        """
        arr, index = operands
        if isinstance(arr, ArrayVariable):
            return

        if isinstance(index, BitVecConstant):
            ival = index.value

            # props are slow and using them in tight loops should be avoided, esp when they offer no additional validation
            # arr._operands[1] = arr.index, arr._operands[0] = arr.array
            while isinstance(arr, ArrayStore) and isinstance(arr._operands[1], BitVecConstant) and arr._operands[1]._value != ival:
                arr = arr._operands[0]  # arr.array

        if isinstance(index, BitVecConstant) and isinstance(arr, ArrayStore) and isinstance(arr.index, BitVecConstant) and arr.index.value == index.value:
            return arr.value
        else:
            if arr is not expression.array:
                return arr.select(index)