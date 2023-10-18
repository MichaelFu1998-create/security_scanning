def split_add_ops(text):
    """Specialized function splitting text at add/sub operators.
    Operands are *not* translated. Example result ['op1', '+', 'op2', '-', 'op3']"""
    n = 0
    text = text.replace('++', '##').replace(
        '--', '@@')  #text does not normally contain any of these
    spotted = False  # set to true if noticed anything other than +- or white space
    last = 0
    while n < len(text):
        e = text[n]
        if e == '+' or e == '-':
            if spotted:
                yield text[last:n].replace('##', '++').replace('@@', '--')
                yield e
                last = n + 1
                spotted = False
        elif e == '/' or e == '*' or e == '%':
            spotted = False
        elif e != ' ':
            spotted = True
        n += 1
    yield text[last:n].replace('##', '++').replace('@@', '--')