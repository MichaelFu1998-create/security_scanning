def t_BYTESM(t):
    r"bytes(?P<nbytes>32|31|30|29|28|27|26|25|24|23|22|21|20|19|18|17|16|15|14|13|12|11|10|9|8|7|6|5|4|3|2|1)"
    size = int(t.lexer.lexmatch.group('nbytes'))
    t.value = ('bytesM', size)
    return t