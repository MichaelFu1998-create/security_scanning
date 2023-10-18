def fix_js_args(func):
    '''Use this function when unsure whether func takes this and arguments as its last 2 args.
       It will append 2 args if it does not.'''
    fcode = six.get_function_code(func)
    fargs = fcode.co_varnames[fcode.co_argcount - 2:fcode.co_argcount]
    if fargs == ('this', 'arguments') or fargs == ('arguments', 'var'):
        return func
    code = append_arguments(six.get_function_code(func), ('this', 'arguments'))

    return types.FunctionType(
        code,
        six.get_function_globals(func),
        func.__name__,
        closure=six.get_function_closure(func))