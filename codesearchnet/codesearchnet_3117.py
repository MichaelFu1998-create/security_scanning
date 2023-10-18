def unify_string_literals(js_string):
    """this function parses the string just like javascript
       for example literal '\d' in JavaScript would be interpreted
       as 'd' - backslash would be ignored and in Pyhon this
       would be interpreted as '\\d' This function fixes this problem."""
    n = 0
    res = ''
    limit = len(js_string)
    while n < limit:
        char = js_string[n]
        if char == '\\':
            new, n = do_escape(js_string, n)
            res += new
        else:
            res += char
            n += 1
    return res