def IIR_sos_header(fname_out, SOS_mat):
    """
    Write IIR SOS Header Files
    File format is compatible with CMSIS-DSP IIR 
    Directform II Filter Functions
    
    Mark Wickert March 2015-October 2016
    """
    Ns, Mcol = SOS_mat.shape
    f = open(fname_out, 'wt')
    f.write('//define a IIR SOS CMSIS-DSP coefficient array\n\n')
    f.write('#include <stdint.h>\n\n')
    f.write('#ifndef STAGES\n')
    f.write('#define STAGES %d\n' % Ns)
    f.write('#endif\n')
    f.write('/*********************************************************/\n');
    f.write('/*                     IIR SOS Filter Coefficients       */\n');
    f.write('float32_t ba_coeff[%d] = { //b0,b1,b2,a1,a2,... by stage\n' % (5 * Ns))
    for k in range(Ns):
        if (k < Ns - 1):
            f.write('    %+-13e, %+-13e, %+-13e,\n' % \
                    (SOS_mat[k, 0], SOS_mat[k, 1], SOS_mat[k, 2]))
            f.write('    %+-13e, %+-13e,\n' % \
                    (-SOS_mat[k, 4], -SOS_mat[k, 5]))
        else:
            f.write('    %+-13e, %+-13e, %+-13e,\n' % \
                    (SOS_mat[k, 0], SOS_mat[k, 1], SOS_mat[k, 2]))
            f.write('    %+-13e, %+-13e\n' % \
                    (-SOS_mat[k, 4], -SOS_mat[k, 5]))
    # for k in range(Ns):
    #     if (k < Ns-1):
    #         f.write('    %15.12f, %15.12f, %15.12f,\n' % \
    #                 (SOS_mat[k,0],SOS_mat[k,1],SOS_mat[k,2]))
    #         f.write('    %15.12f, %15.12f,\n' % \
    #                 (-SOS_mat[k,4],-SOS_mat[k,5]))
    #     else:
    #         f.write('    %15.12f, %15.12f, %15.12f,\n' % \
    #                 (SOS_mat[k,0],SOS_mat[k,1],SOS_mat[k,2]))
    #         f.write('    %15.12f, %15.12f\n' % \
    #                 (-SOS_mat[k,4],-SOS_mat[k,5]))
    f.write('};\n')
    f.write('/*********************************************************/\n')
    f.close()