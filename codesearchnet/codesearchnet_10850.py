def traceback_plot(self,fsize=(6,4)):
        """
        Plots a path of the possible last 4 states.

        Parameters
        ----------
        fsize : Plot size for matplotlib.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> from sk_dsp_comm import digitalcom as dc
        >>> import numpy as np
        >>> cc = fec_conv()
        >>> x = np.random.randint(0,2,100)
        >>> state = '00'
        >>> y,state = cc.conv_encoder(x,state)
        >>> # Add channel noise to bits translated to +1/-1
        >>> yn = dc.cpx_AWGN(2*y-1,5,1) # SNR = 5 dB
        >>> # Translate noisy +1/-1 bits to soft values on [0,7]
        >>> yn = (yn.real+1)/2*7
        >>> z = cc.viterbi_decoder(yn)
        >>> cc.traceback_plot()
        >>> plt.show()
        """
        traceback_states = self.paths.traceback_states
        plt.figure(figsize=fsize)
        plt.axis([-self.decision_depth+1, 0, 
                  -(self.Nstates-1)-0.5, 0.5])
        M,N = traceback_states.shape
        traceback_states = -traceback_states[:,::-1]

        plt.plot(range(-(N-1),0+1),traceback_states.T)
        plt.xlabel('Traceback Symbol Periods')
        plt.ylabel('State Index $0$ to -$2^{(K-1)}$')
        plt.title('Survivor Paths Traced Back From All %d States' % self.Nstates)
        plt.grid()