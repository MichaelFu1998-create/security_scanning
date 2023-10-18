def t_UINTN(t):
    r"uint(?P<size>256|248|240|232|224|216|208|200|192|184|176|168|160|152|144|136|128|120|112|104|96|88|80|72|64|56|48|40|32|24|16|8)"
    size = int(t.lexer.lexmatch.group('size'))
    t.value = ('uint', size)
    return t