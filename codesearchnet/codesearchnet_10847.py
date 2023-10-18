def puncture(self,code_bits,puncture_pattern = ('110','101')):
        """
        Apply puncturing to the serial bits produced by convolutionally
        encoding.

        :param code_bits:
        :param puncture_pattern:
        :return:

        Examples
        --------
        This example uses the following puncture matrix:

        .. math::

           \\begin{align*}
               \\mathbf{A} = \\begin{bmatrix}
                1 & 1 & 0 \\\\
                1 & 0 & 1
                \\end{bmatrix}
           \\end{align*}

        The upper row operates on the outputs for the :math:`G_{1}` polynomial and the lower row operates on the outputs of
        the  :math:`G_{2}`  polynomial.

        >>> import numpy as np
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> cc = fec_conv(('101','111'))
        >>> x = np.array([0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
        >>> state = '00'
        >>> y, state = cc.conv_encoder(x, state)
        >>> cc.puncture(y, ('110','101'))
        array([ 0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  1.,  1.,  0.,  0.])
        """
        # Check to see that the length of code_bits is consistent with a rate
        # 1/2 code.
        L_pp = len(puncture_pattern[0])
        N_codewords = int(np.floor(len(code_bits)/float(2)))
        if 2*N_codewords != len(code_bits):
            warnings.warn('Number of code bits must be even!')
            warnings.warn('Truncating bits to be compatible.')
            code_bits = code_bits[:2*N_codewords]
        # Extract the G1 and G2 encoded bits from the serial stream.
        # Assume the stream is of the form [G1 G2 G1 G2 ...   ]
        x_G1 = code_bits.reshape(N_codewords,2).take([0],
                                 axis=1).reshape(1,N_codewords).flatten()
        x_G2 = code_bits.reshape(N_codewords,2).take([1],
                                 axis=1).reshape(1,N_codewords).flatten()
        # Check to see that the length of x_G1 and x_G2 is consistent with the
        # length of the puncture pattern
        N_punct_periods = int(np.floor(N_codewords/float(L_pp)))
        if L_pp*N_punct_periods != N_codewords:
            warnings.warn('Code bit length is not a multiple pp = %d!' % L_pp)
            warnings.warn('Truncating bits to be compatible.')
            x_G1 = x_G1[:L_pp*N_punct_periods]
            x_G2 = x_G2[:L_pp*N_punct_periods]
        #Puncture x_G1 and x_G1
        g1_pp1 = [k for k,g1 in enumerate(puncture_pattern[0]) if g1 == '1']
        g2_pp1 = [k for k,g2 in enumerate(puncture_pattern[1]) if g2 == '1']
        N_pp = len(g1_pp1)
        y_G1 = x_G1.reshape(N_punct_periods,L_pp).take(g1_pp1,
                            axis=1).reshape(N_pp*N_punct_periods,1)
        y_G2 = x_G2.reshape(N_punct_periods,L_pp).take(g2_pp1,
                            axis=1).reshape(N_pp*N_punct_periods,1)
        # Interleave y_G1 and y_G2 for modulation via a serial bit stream
        y = np.hstack((y_G1,y_G2)).reshape(1,2*N_pp*N_punct_periods).flatten()
        return y