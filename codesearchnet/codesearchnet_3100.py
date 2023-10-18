def transform_crap(code):  #needs some more tests
    """Transforms this ?: crap into if else python syntax"""
    ind = code.rfind('?')
    if ind == -1:
        return code
    sep = code.find(':', ind)
    if sep == -1:
        raise SyntaxError('Invalid ?: syntax (probably missing ":" )')
    beg = max(code.rfind(':', 0, ind), code.find('?', 0, ind)) + 1
    end = code.find(':', sep + 1)
    end = len(code) if end == -1 else end
    formula = '(' + code[ind + 1:sep] + ' if ' + code[
        beg:ind] + ' else ' + code[sep + 1:end] + ')'
    return transform_crap(code[:beg] + formula + code[end:])