def declaration(function):
    '''
    Declare abstract function. 
    
    Requires function to be empty except for docstring describing semantics.
    To apply function, first argument must come with implementation of semantics.
    '''
    function,name=_strip_function(function)
    if not function.__code__.co_code in [empty_function.__code__.co_code, doc_string_only_function.__code__.co_code]: 
        raise ValueError('Declaration requires empty function definition')
    def not_implemented_function(*args,**kwargs):
        raise ValueError('Argument \'{}\' did not specify how \'{}\' should act on it'.format(args[0],name))
    not_implemented_function.__qualname__=not_implemented_function.__name__ 
    return default(not_implemented_function,name=name)