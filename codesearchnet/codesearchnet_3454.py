def input_from_cons(constupl, datas):
    ' solve bytes in |datas| based on '
    def make_chr(c):
        try:
            return chr(c)
        except Exception:
            return c
    newset = constraints_to_constraintset(constupl)

    ret = ''
    for data in datas:
        for c in data:
            ret += make_chr(solver.get_value(newset, c))
    return ret