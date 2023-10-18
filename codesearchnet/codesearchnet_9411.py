def _eval_arg_type(arg_type, T=Any, arg=None, sig=None):
    """Returns a type from a snippit of python source. Should normally be
    something just like 'str' or 'Object'.

        arg_type            the source to be evaluated
        T                         the default type
        arg                     context of where this type was extracted
        sig                     context from where the arg was extracted

    Returns a type or a Type
    """
    try:
        T = eval(arg_type)
    except Exception as e:
        raise ValueError('The type of {0} could not be evaluated in {1} for {2}: {3}' \
            .format(arg_type, arg, sig, text_type(e)))
    else:
        if type(T) not in (type, Type):
            raise TypeError('{0} is not a valid type in {1} for {2}' \
                .format(repr(T), arg, sig))
        return T