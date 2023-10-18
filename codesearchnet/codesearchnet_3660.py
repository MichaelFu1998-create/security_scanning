def taint_with(arg, taint, value_bits=256, index_bits=256):
    """
    Helper to taint a value.
    :param arg: a value or Expression
    :param taint: a regular expression matching a taint value (eg. 'IMPORTANT.*'). If None, this function checks for any taint value.
    """
    from ..core.smtlib import BitVecConstant  # prevent circular imports

    tainted_fset = frozenset((taint,))

    if not issymbolic(arg):
        if isinstance(arg, int):
            arg = BitVecConstant(value_bits, arg)
            arg._taint = tainted_fset
        else:
            raise ValueError("type not supported")

    else:
        arg = copy.copy(arg)
        arg._taint |= tainted_fset

    return arg