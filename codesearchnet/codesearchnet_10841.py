def conv_Pb_bound(R,dfree,Ck,SNRdB,hard_soft,M=2):
    """
    Coded bit error probabilty

    Convolution coding bit error probability upper bound
    according to Ziemer & Peterson 7-16, p. 507
    
    Mark Wickert November 2014

    Parameters
    ----------
    R: Code rate
    dfree: Free distance of the code
    Ck: Weight coefficient
    SNRdB: Signal to noise ratio in dB
    hard_soft: 0 hard, 1 soft, 2 uncoded
    M: M-ary

    Examples
    --------
    >>> import numpy as np
    >>> from sk_dsp_comm import fec_conv as fec
    >>> import matplotlib.pyplot as plt
    >>> SNRdB = np.arange(2,12,.1)
    >>> Pb = fec.conv_Pb_bound(1./2,10,[36, 0, 211, 0, 1404, 0, 11633],SNRdB,2)
    >>> Pb_1_2 = fec.conv_Pb_bound(1./2,10,[36, 0, 211, 0, 1404, 0, 11633],SNRdB,1)
    >>> Pb_3_4 = fec.conv_Pb_bound(3./4,4,[164, 0, 5200, 0, 151211, 0, 3988108],SNRdB,1)
    >>> plt.semilogy(SNRdB,Pb)
    >>> plt.semilogy(SNRdB,Pb_1_2)
    >>> plt.semilogy(SNRdB,Pb_3_4)
    >>> plt.axis([2,12,1e-7,1e0])
    >>> plt.xlabel(r'$E_b/N_0$ (dB)')
    >>> plt.ylabel(r'Symbol Error Probability')
    >>> plt.legend(('Uncoded BPSK','R=1/2, K=7, Soft','R=3/4 (punc), K=7, Soft'),loc='best')
    >>> plt.grid();
    >>> plt.show()

    Notes
    -----
    The code rate R is given by :math:`R_{s} = \\frac{k}{n}`.
    Mark Wickert and Andrew Smit 2018
    """
    Pb = np.zeros_like(SNRdB)
    SNR = 10.**(SNRdB/10.)

    for n,SNRn in enumerate(SNR):
        for k in range(dfree,len(Ck)+dfree):
            if hard_soft == 0: # Evaluate hard decision bound
                Pb[n] += Ck[k-dfree]*hard_Pk(k,R,SNRn,M)
            elif hard_soft == 1: # Evaluate soft decision bound
                Pb[n] += Ck[k-dfree]*soft_Pk(k,R,SNRn,M)
            else: # Compute Uncoded Pe
                if M == 2:
                    Pb[n] = Q_fctn(np.sqrt(2.*SNRn))
                else:
                    Pb[n] = 4./np.log2(M)*(1 - 1/np.sqrt(M))*\
                            np.gaussQ(np.sqrt(3*np.log2(M)/(M-1)*SNRn));
    return Pb