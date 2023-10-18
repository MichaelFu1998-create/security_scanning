def remove_objects(code, count=1):
    """ This function replaces objects with OBJECTS_LVALS, returns new code, replacement dict and count.
        count arg is the number that should be added to the LVAL of the first replaced object
    """
    replacements = {}  #replacement dict
    br = bracket_split(code, ['{}', '[]'])
    res = ''
    last = ''
    for e in br:
        #test whether e is an object
        if e[0] == '{':
            n, temp_rep, cand_count = remove_objects(e[1:-1], count)
            # if e was not an object then n should not contain any :
            if is_object(n, last):
                #e was an object
                res += ' ' + OBJECT_LVAL % count
                replacements[OBJECT_LVAL % count] = e
                count += 1
            else:
                # e was just a code block but could contain objects inside
                res += '{%s}' % n
                count = cand_count
                replacements.update(temp_rep)
        elif e[0] == '[':
            if is_array(last):
                res += e  # will be translated later
            else:  # prop get
                n, rep, count = remove_objects(e[1:-1], count)
                res += '[%s]' % n
                replacements.update(rep)
        else:  # e does not contain any objects
            res += e
        last = e  #needed to test for this stipid empty object
    return res, replacements, count