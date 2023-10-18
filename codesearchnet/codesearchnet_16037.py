def _get_name_info(name_index, name_list):
    """Helper to get optional details about named references

       Returns the dereferenced name as both value and repr if the name
       list is defined.
       Otherwise returns the name index and its repr().
    """
    argval = name_index
    if name_list is not None:
        try:
            argval = name_list[name_index]
        except IndexError:
            raise ValidationError("Names value out of range: {}".format(name_index)) from None
        argrepr = argval
    else:
        argrepr = repr(argval)
    return argval, argrepr