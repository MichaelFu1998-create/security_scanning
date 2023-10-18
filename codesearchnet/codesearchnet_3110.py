def remove_arrays(code, count=1):
    """removes arrays and replaces them with ARRAY_LVALS
       returns new code and replacement dict
       *NOTE* has to be called AFTER remove objects"""
    res = ''
    last = ''
    replacements = {}
    for e in bracket_split(code, ['[]']):
        if e[0] == '[':
            if is_array(last):
                name = ARRAY_LVAL % count
                res += ' ' + name
                replacements[name] = e
                count += 1
            else:  # pseudo array. But pseudo array can contain true array. for example a[['d'][3]] has 2 pseudo and 1 true array
                cand, new_replacements, count = remove_arrays(e[1:-1], count)
                res += '[%s]' % cand
                replacements.update(new_replacements)
        else:
            res += e
        last = e
    return res, replacements, count