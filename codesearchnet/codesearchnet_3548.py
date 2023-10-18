def to_constant(expression):
    """
        Iff the expression can be simplified to a Constant get the actual concrete value.
        This discards/ignore any taint
    """
    value = simplify(expression)
    if isinstance(value, Expression) and value.taint:
        raise ValueError("Can not simplify tainted values to constant")
    if isinstance(value, Constant):
        return value.value
    elif isinstance(value, Array):
        if expression.index_max:
            ba = bytearray()
            for i in range(expression.index_max):
                value_i = simplify(value[i])
                if not isinstance(value_i, Constant):
                    break
                ba.append(value_i.value)
            else:
                return bytes(ba)
            return expression
    return value