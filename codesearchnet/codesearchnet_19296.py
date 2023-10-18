def standardize_variables(sentence, dic=None):
    """Replace all the variables in sentence with new variables.
    >>> e = expr('F(a, b, c) & G(c, A, 23)')
    >>> len(variables(standardize_variables(e)))
    3
    >>> variables(e).intersection(variables(standardize_variables(e)))
    set([])
    >>> is_variable(standardize_variables(expr('x')))
    True
    """
    if dic is None: dic = {}
    if not isinstance(sentence, Expr):
        return sentence
    elif is_var_symbol(sentence.op):
        if sentence in dic:
            return dic[sentence]
        else:
            v = Expr('v_%d' % standardize_variables.counter.next())
            dic[sentence] = v
            return v
    else:
        return Expr(sentence.op,
                    *[standardize_variables(a, dic) for a in sentence.args])