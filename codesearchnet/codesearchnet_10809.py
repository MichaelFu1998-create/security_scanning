def FIR_fix_header(fname_out, h):
    """
    Write FIR Fixed-Point Filter Header Files 
    
    Mark Wickert February 2015
    """
    M = len(h)
    hq = int16(rint(h * 2 ** 15))
    N = 8  # Coefficients per line
    f = open(fname_out, 'wt')
    f.write('//define a FIR coefficient Array\n\n')
    f.write('#include <stdint.h>\n\n')
    f.write('#ifndef M_FIR\n')
    f.write('#define M_FIR %d\n' % M)
    f.write('#endif\n')
    f.write('/************************************************************************/\n');
    f.write('/*                         FIR Filter Coefficients                      */\n');
    f.write('int16_t h_FIR[M_FIR] = {')
    kk = 0;
    for k in range(M):
        # k_mod = k % M
        if (kk < N - 1) and (k < M - 1):
            f.write('%5d,' % hq[k])
            kk += 1
        elif (kk == N - 1) & (k < M - 1):
            f.write('%5d,\n' % hq[k])
            if k < M:
                f.write('                        ')
                kk = 0
        else:
            f.write('%5d' % hq[k])
    f.write('};\n')
    f.write('/************************************************************************/\n')
    f.close()