def pythonize_arguments(arg_str):
    """
    Remove types from function arguments in cython
    """
    out_args = []
    # If there aren't any arguments return the empty string
    if arg_str is None:
        return out_str
    args = arg_str.split(',')
    for arg in args:
        components = arg.split('=')
        name_and_type=components[0].split(' ')
        # There is probably type info
        if name_and_type[-1]=='' and len(name_and_type)>1:
            name=name_and_type[-2]
        else:
            name=name_and_type[-1]
        # if there are default parameters
        if len(components)>1:
            name+='='+components[1]

        out_args.append(name)
    return ','.join(out_args)