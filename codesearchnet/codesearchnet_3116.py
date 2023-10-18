def recover_constants(py_source,
                      replacements):  #now has n^2 complexity. improve to n
    '''Converts identifiers representing Js constants to the PyJs constants
    PyJsNumberConst_1_ which has the true value of 5 will be converted to PyJsNumber(5)'''
    for identifier, value in replacements.iteritems():
        if identifier.startswith('PyJsConstantRegExp'):
            py_source = py_source.replace(identifier,
                                          'JsRegExp(%s)' % repr(value))
        elif identifier.startswith('PyJsConstantString'):
            py_source = py_source.replace(
                identifier, 'Js(u%s)' % unify_string_literals(value))
        else:
            py_source = py_source.replace(identifier, 'Js(%s)' % value)
    return py_source