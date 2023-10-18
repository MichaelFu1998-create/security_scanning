def t_TOKEN(t):
    '[a-zA-Z0-9]+'
    #print t.value,t.lexer.lexdata[t.lexer.lexpos-len(t.value):],re_TYPE.match(t.lexer.lexdata,t.lexer.lexpos-len(t.value))
    if re_TYPE.match(t.value):
        t.type = 'TYPE'
    elif re_PTR.match(t.value):
        t.type = 'PTR'
    elif re_NUMBER.match(t.value):
        if t.value.startswith('0x'):
            t.value = t.value[2:]
        t.value = int(t.value, 16)
        t.type = 'NUMBER'
    elif re_REGISTER.match(t.value):
        t.type = 'REGISTER'
    elif re_SEGMENT.match(t.value):
        t.type = 'SEGMENT'
    else:
        raise Exception(f"Unknown:<{t.value}>")
    return t