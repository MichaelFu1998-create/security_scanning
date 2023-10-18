def run_file(path_or_file, context=None):
    ''' Context must be EvalJS object. Runs given path as a JS program. Returns (eval_value, context).
    '''
    if context is None:
        context = EvalJs()
    if not isinstance(context, EvalJs):
        raise TypeError('context must be the instance of EvalJs')
    eval_value = context.eval(get_file_contents(path_or_file))
    return eval_value, context