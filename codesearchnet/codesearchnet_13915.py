def draw_cornu_flat(x0, y0, t0, t1, s0, c0, flip, cs, ss, cmd):
    
    """ Raph Levien's code draws fast LINETO segments.
    """
    
    for j in range(0, 100):
        t = j * .01
        s, c = eval_cornu(t0 + t * (t1 - t0))
        s *= flip
        s -= s0
        c -= c0
        #print '%', c, s
        x = c * cs - s * ss
        y = s * cs + c * ss
        print_pt(x0 + x, y0 + y, cmd)
        cmd = 'lineto'
    return cmd