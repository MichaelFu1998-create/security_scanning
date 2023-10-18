def p_expression_deref(p):
    'expression : TYPE PTR LBRAKET expression RBRAKET'
    size = sizes[p[1]]
    address = p[4]
    char_list = functions['read_memory'](address, size)
    value = Operators.CONCAT(8 * len(char_list), *reversed(map(Operators.ORD, char_list)))
    p[0] = value