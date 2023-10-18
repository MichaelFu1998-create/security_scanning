def p_dynamic_fixed_type(p):
    """
     T : T LBRAKET NUMBER RBRAKET
    """
    reps = int(p[3])
    base_type = p[1]
    p[0] = ('array', reps, base_type)