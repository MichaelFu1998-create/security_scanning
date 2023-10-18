def CA_code_header(fname_out, Nca):
    """
    Write 1023 bit CA (Gold) Code Header Files

    Mark Wickert February 2015
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ca = loadtxt(dir_path + '/ca1thru37.txt', dtype=int16, usecols=(Nca - 1,), unpack=True)

    M = 1023  # code period
    N = 23  # code bits per line
    Sca = 'ca' + str(Nca)
    f = open(fname_out, 'wt')
    f.write('//define a CA code\n\n')
    f.write('#include <stdint.h>\n\n')
    f.write('#ifndef N_CA\n')
    f.write('#define N_CA %d\n' % M)
    f.write('#endif\n')
    f.write('/*******************************************************************/\n');
    f.write('/*                    1023 Bit CA Gold Code %2d                     */\n' \
            % Nca);
    f.write('int8_t ca%d[N_CA] = {' % Nca)
    kk = 0;
    for k in range(M):
        # k_mod = k % M
        if (kk < N - 1) and (k < M - 1):
            f.write('%d,' % ca[k])
            kk += 1
        elif (kk == N - 1) & (k < M - 1):
            f.write('%d,\n' % ca[k])
            if k < M:
                if Nca < 10:
                    f.write('                    ')
                else:
                    f.write('                     ')
                kk = 0
        else:
            f.write('%d' % ca[k])
    f.write('};\n')
    f.write('/*******************************************************************/\n')
    f.close()