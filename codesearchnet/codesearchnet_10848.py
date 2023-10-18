def depuncture(self,soft_bits,puncture_pattern = ('110','101'),
                   erase_value = 3.5):
        """
        Apply de-puncturing to the soft bits coming from the channel. Erasure bits
        are inserted to return the soft bit values back to a form that can be
        Viterbi decoded.

        :param soft_bits:
        :param puncture_pattern:
        :param erase_value:
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
        >>> yp = cc.puncture(y, ('110','101'))
        >>> cc.depuncture(yp, ('110', '101'), 1)
        array([ 0., 0., 0., 1., 1., 1., 1., 0., 0., 1., 1., 0., 1., 1., 0., 1., 1., 0.]
        """
        # Check to see that the length of soft_bits is consistent with a rate
        # 1/2 code.
        L_pp = len(puncture_pattern[0])
        L_pp1 = len([g1 for g1 in puncture_pattern[0] if g1 == '1'])
        L_pp0 = len([g1 for g1 in puncture_pattern[0] if g1 == '0'])
        #L_pp0 = len([g1 for g1 in pp1 if g1 == '0'])
        N_softwords = int(np.floor(len(soft_bits)/float(2)))
        if 2*N_softwords != len(soft_bits):
            warnings.warn('Number of soft bits must be even!')
            warnings.warn('Truncating bits to be compatible.')
            soft_bits = soft_bits[:2*N_softwords]
        # Extract the G1p and G2p encoded bits from the serial stream.
        # Assume the stream is of the form [G1p G2p G1p G2p ...   ],
        # which for QPSK may be of the form [Ip Qp Ip Qp Ip Qp ...    ]
        x_G1 = soft_bits.reshape(N_softwords,2).take([0],
                                 axis=1).reshape(1,N_softwords).flatten()
        x_G2 = soft_bits.reshape(N_softwords,2).take([1],
                                 axis=1).reshape(1,N_softwords).flatten()
        # Check to see that the length of x_G1 and x_G2 is consistent with the
        # puncture length period of the soft bits
        N_punct_periods = int(np.floor(N_softwords/float(L_pp1)))
        if L_pp1*N_punct_periods != N_softwords:
            warnings.warn('Number of soft bits per puncture period is %d' % L_pp1)
            warnings.warn('The number of soft bits is not a multiple')
            warnings.warn('Truncating soft bits to be compatible.')
            x_G1 = x_G1[:L_pp1*N_punct_periods]
            x_G2 = x_G2[:L_pp1*N_punct_periods]
        x_G1 = x_G1.reshape(N_punct_periods,L_pp1)
        x_G2 = x_G2.reshape(N_punct_periods,L_pp1)
        #Depuncture x_G1 and x_G1
        g1_pp1 = [k for k,g1 in enumerate(puncture_pattern[0]) if g1 == '1']
        g1_pp0 = [k for k,g1 in enumerate(puncture_pattern[0]) if g1 == '0']
        g2_pp1 = [k for k,g2 in enumerate(puncture_pattern[1]) if g2 == '1']
        g2_pp0 = [k for k,g2 in enumerate(puncture_pattern[1]) if g2 == '0']
        x_E = erase_value*np.ones((N_punct_periods,L_pp0))
        y_G1 = np.hstack((x_G1,x_E))
        y_G2 = np.hstack((x_G2,x_E))
        [g1_pp1.append(val) for idx,val in enumerate(g1_pp0)]
        g1_comp = list(zip(g1_pp1,list(range(L_pp))))
        g1_comp.sort()
        G1_col_permute = [g1_comp[idx][1] for idx in range(L_pp)]
        [g2_pp1.append(val) for idx,val in enumerate(g2_pp0)]
        g2_comp = list(zip(g2_pp1,list(range(L_pp))))
        g2_comp.sort()
        G2_col_permute = [g2_comp[idx][1] for idx in range(L_pp)]
        #permute columns to place erasure bits in the correct position
        y = np.hstack((y_G1[:,G1_col_permute].reshape(L_pp*N_punct_periods,1),
                       y_G2[:,G2_col_permute].reshape(L_pp*N_punct_periods,
                       1))).reshape(1,2*L_pp*N_punct_periods).flatten()
        return y