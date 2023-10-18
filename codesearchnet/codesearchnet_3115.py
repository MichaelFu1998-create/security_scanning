def remove_constants(source):
    '''Replaces Strings and Regexp literals in the source code with
       identifiers and *removes comments*. Identifier is of the format:

       PyJsStringConst(String const number)_ - for Strings
       PyJsRegExpConst(RegExp const number)_ - for RegExps

       Returns dict which relates identifier and replaced constant.

       Removes single line and multiline comments from JavaScript source code
       Pseudo comments (inside strings) will not be removed.

       For example this line:
       var x = "/*PSEUDO COMMENT*/ TEXT //ANOTHER PSEUDO COMMENT"
       will be unaltered'''
    source = ' ' + source + '\n'
    comments = []
    inside_comment, single_comment = False, False
    inside_single, inside_double = False, False
    inside_regexp = False
    regexp_class_count = 0
    n = 0
    while n < len(source):
        char = source[n]
        if char == '"' and not (inside_comment or inside_single
                                or inside_regexp):
            if not _is_cancelled(source, n):
                if inside_double:
                    inside_double[1] = n + 1
                    comments.append(inside_double)
                    inside_double = False
                else:
                    inside_double = [n, None, 0]
        elif char == "'" and not (inside_comment or inside_double
                                  or inside_regexp):
            if not _is_cancelled(source, n):
                if inside_single:
                    inside_single[1] = n + 1
                    comments.append(inside_single)
                    inside_single = False
                else:
                    inside_single = [n, None, 0]
        elif (inside_single or inside_double):
            if char in LINE_TERMINATOR:
                if _is_cancelled(source, n):
                    if char == CR and source[n + 1] == LF:
                        n += 1
                    n += 1
                    continue
                else:
                    raise SyntaxError(
                        'Invalid string literal. Line terminators must be escaped!'
                    )
        else:
            if inside_comment:
                if single_comment:
                    if char in LINE_TERMINATOR:
                        inside_comment[1] = n
                        comments.append(inside_comment)
                        inside_comment = False
                        single_comment = False
                else:  # Multiline
                    if char == '/' and source[n - 1] == '*':
                        inside_comment[1] = n + 1
                        comments.append(inside_comment)
                        inside_comment = False
            elif inside_regexp:
                if not quiting_regexp:
                    if char in LINE_TERMINATOR:
                        raise SyntaxError(
                            'Invalid regexp literal. Line terminators cant appear!'
                        )
                    if _is_cancelled(source, n):
                        n += 1
                        continue
                    if char == '[':
                        regexp_class_count += 1
                    elif char == ']':
                        regexp_class_count = max(regexp_class_count - 1, 0)
                    elif char == '/' and not regexp_class_count:
                        quiting_regexp = True
                else:
                    if char not in IDENTIFIER_START:
                        inside_regexp[1] = n
                        comments.append(inside_regexp)
                        inside_regexp = False
            elif char == '/' and source[n - 1] == '/':
                single_comment = True
                inside_comment = [n - 1, None, 1]
            elif char == '*' and source[n - 1] == '/':
                inside_comment = [n - 1, None, 1]
            elif char == '/' and source[n + 1] not in ('/', '*'):
                if not _ensure_regexp(source, n):  #<- improve this one
                    n += 1
                    continue  #Probably just a division
                quiting_regexp = False
                inside_regexp = [n, None, 2]
            elif not (inside_comment or inside_regexp):
                if (char in NUMS and
                        source[n - 1] not in IDENTIFIER_PART) or char == '.':
                    if char == '.':
                        k = parse_num(source, n + 1, NUMS)
                        if k == n + 1:  # just a stupid dot...
                            n += 1
                            continue
                        k = parse_exponent(source, k)
                    elif char == '0' and source[n + 1] in {
                            'x', 'X'
                    }:  #Hex number probably
                        k = parse_num(source, n + 2, HEX)
                        if k == n + 2 or source[k] in IDENTIFIER_PART:
                            raise SyntaxError('Invalid hex literal!')
                    else:  #int or exp or flot or exp flot
                        k = parse_num(source, n + 1, NUMS)
                        if source[k] == '.':
                            k = parse_num(source, k + 1, NUMS)
                        k = parse_exponent(source, k)
                    comments.append((n, k, 3))
                    n = k
                    continue
        n += 1
    res = ''
    start = 0
    count = 0
    constants = {}
    for end, next_start, typ in comments:
        res += source[start:end]
        start = next_start
        if typ == 0:  # String
            name = StringName
        elif typ == 1:  # comment
            continue
        elif typ == 2:  # regexp
            name = RegExpName
        elif typ == 3:  # number
            name = NumberName
        else:
            raise RuntimeError()
        res += ' ' + name % count + ' '
        constants[name % count] = source[end:next_start]
        count += 1
    res += source[start:]
    # remove this stupid white space
    for e in WHITE:
        res = res.replace(e, ' ')
    res = res.replace(CR + LF, '\n')
    for e in LINE_TERMINATOR:
        res = res.replace(e, '\n')
    return res.strip(), constants