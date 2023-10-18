def _get_const_info(const_index, const_list):
    """
    Helper to get optional details about const references

       Returns the dereferenced constant and its repr if the constant
       list is defined.
       Otherwise returns the constant index and its repr().
    """
    argval = const_index
    if const_list is not None:
        try:
            argval = const_list[const_index]
        except IndexError:
            raise ValidationError("Consts value out of range: {}".format(const_index)) from None
    return argval, repr(argval)