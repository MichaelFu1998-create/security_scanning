def p_expression_derefseg(p):
    'expression : TYPE PTR SEGMENT COLOM LBRAKET expression RBRAKET'
    size = sizes[p[1]]
    address = p[6]
    seg = functions['read_register'](p[3])
    base, limit, _ = functions['get_descriptor'](seg)
    address = base + address
    char_list = functions['read_memory'](address, size)
    value = Operators.CONCAT(8 * len(char_list), *reversed(map(Operators.ORD, char_list)))
    p[0] = value