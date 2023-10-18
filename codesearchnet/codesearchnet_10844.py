def viterbi_decoder(self,x,metric_type='soft',quant_level=3):
        """
        A method which performs Viterbi decoding of noisy bit stream,
        taking as input soft bit values centered on +/-1 and returning 
        hard decision 0/1 bits.

        Parameters
        ----------
        x: Received noisy bit values centered on +/-1 at one sample per bit
        metric_type: 
            'hard' - Hard decision metric. Expects binary or 0/1 input values.
            'unquant' - unquantized soft decision decoding. Expects +/-1
                input values.
            'soft' - soft decision decoding.
        quant_level: The quantization level for soft decoding. Expected 
        input values between 0 and 2^quant_level-1. 0 represents the most 
        confident 0 and 2^quant_level-1 represents the most confident 1. 
        Only used for 'soft' metric type.

        Returns
        -------
        y: Decoded 0/1 bit stream

        Examples
        --------
        >>> import numpy as np
        >>> from numpy.random import randint
        >>> import sk_dsp_comm.fec_conv as fec
        >>> import sk_dsp_comm.digitalcom as dc
        >>> import matplotlib.pyplot as plt
        >>> # Soft decision rate 1/2 simulation
        >>> N_bits_per_frame = 10000
        >>> EbN0 = 4
        >>> total_bit_errors = 0
        >>> total_bit_count = 0
        >>> cc1 = fec.fec_conv(('11101','10011'),25)
        >>> # Encode with shift register starting state of '0000'
        >>> state = '0000'
        >>> while total_bit_errors < 100:
        >>>     # Create 100000 random 0/1 bits
        >>>     x = randint(0,2,N_bits_per_frame)
        >>>     y,state = cc1.conv_encoder(x,state)
        >>>     # Add channel noise to bits, include antipodal level shift to [-1,1]
        >>>     yn_soft = dc.cpx_AWGN(2*y-1,EbN0-3,1) # Channel SNR is 3 dB less for rate 1/2
        >>>     yn_hard = ((np.sign(yn_soft.real)+1)/2).astype(int)
        >>>     z = cc1.viterbi_decoder(yn_hard,'hard')
        >>>     # Count bit errors
        >>>     bit_count, bit_errors = dc.bit_errors(x,z)
        >>>     total_bit_errors += bit_errors
        >>>     total_bit_count += bit_count
        >>>     print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                    (total_bit_count, total_bit_errors,\
                    total_bit_errors/total_bit_count))
        >>> print('*****************************************************')
        >>> print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                (total_bit_count, total_bit_errors,\
                total_bit_errors/total_bit_count))
        Rate 1/2 Object
        kmax =  0, taumax = 0
        Bits Received = 9976, Bit errors = 77, BEP = 7.72e-03
        kmax =  0, taumax = 0
        Bits Received = 19952, Bit errors = 175, BEP = 8.77e-03
        *****************************************************
        Bits Received = 19952, Bit errors = 175, BEP = 8.77e-03


        >>> # Consider the trellis traceback after the sim completes
        >>> cc1.traceback_plot()
        >>> plt.show()


        >>> # Compare a collection of simulation results with soft decision
        >>> # bounds
        >>> SNRdB = np.arange(0,12,.1)
        >>> Pb_uc = fec.conv_Pb_bound(1/3,7,[4, 12, 20, 72, 225],SNRdB,2)
        >>> Pb_s_third_3 = fec.conv_Pb_bound(1/3,8,[3, 0, 15],SNRdB,1)
        >>> Pb_s_third_4 = fec.conv_Pb_bound(1/3,10,[6, 0, 6, 0],SNRdB,1)
        >>> Pb_s_third_5 = fec.conv_Pb_bound(1/3,12,[12, 0, 12, 0, 56],SNRdB,1)
        >>> Pb_s_third_6 = fec.conv_Pb_bound(1/3,13,[1, 8, 26, 20, 19, 62],SNRdB,1)
        >>> Pb_s_third_7 = fec.conv_Pb_bound(1/3,14,[1, 0, 20, 0, 53, 0, 184],SNRdB,1)
        >>> Pb_s_third_8 = fec.conv_Pb_bound(1/3,16,[1, 0, 24, 0, 113, 0, 287, 0],SNRdB,1)
        >>> Pb_s_half = fec.conv_Pb_bound(1/2,7,[4, 12, 20, 72, 225],SNRdB,1)
        >>> plt.figure(figsize=(5,5))
        >>> plt.semilogy(SNRdB,Pb_uc)
        >>> plt.semilogy(SNRdB,Pb_s_third_3,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_4,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_5,'g')
        >>> plt.semilogy(SNRdB,Pb_s_third_6,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_7,'--')
        >>> plt.semilogy(SNRdB,Pb_s_third_8,'--')
        >>> plt.semilogy([0,1,2,3,4,5],[9.08e-02,2.73e-02,6.52e-03,\
                                8.94e-04,8.54e-05,5e-6],'gs')
        >>> plt.axis([0,12,1e-7,1e0])
        >>> plt.title(r'Soft Decision Rate 1/2 Coding Measurements')
        >>> plt.xlabel(r'$E_b/N_0$ (dB)')
        >>> plt.ylabel(r'Symbol Error Probability')
        >>> plt.legend(('Uncoded BPSK','R=1/3, K=3, Soft',\
                    'R=1/3, K=4, Soft','R=1/3, K=5, Soft',\
                    'R=1/3, K=6, Soft','R=1/3, K=7, Soft',\
                    'R=1/3, K=8, Soft','R=1/3, K=5, Sim', \
                    'Simulation'),loc='upper right')
        >>> plt.grid();
        >>> plt.show()


        >>> # Hard decision rate 1/3 simulation
        >>> N_bits_per_frame = 10000
        >>> EbN0 = 3
        >>> total_bit_errors = 0
        >>> total_bit_count = 0
        >>> cc2 = fec.fec_conv(('11111','11011','10101'),25)
        >>> # Encode with shift register starting state of '0000'
        >>> state = '0000'
        >>> while total_bit_errors < 100:
        >>>     # Create 100000 random 0/1 bits
        >>>     x = randint(0,2,N_bits_per_frame)
        >>>     y,state = cc2.conv_encoder(x,state)
        >>>     # Add channel noise to bits, include antipodal level shift to [-1,1]
        >>>     yn_soft = dc.cpx_AWGN(2*y-1,EbN0-10*np.log10(3),1) # Channel SNR is 10*log10(3) dB less
        >>>     yn_hard = ((np.sign(yn_soft.real)+1)/2).astype(int)
        >>>     z = cc2.viterbi_decoder(yn_hard.real,'hard')
        >>>     # Count bit errors
        >>>     bit_count, bit_errors = dc.bit_errors(x,z)
        >>>     total_bit_errors += bit_errors
        >>>     total_bit_count += bit_count
        >>>     print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                    (total_bit_count, total_bit_errors,\
                    total_bit_errors/total_bit_count))
        >>> print('*****************************************************')
        >>> print('Bits Received = %d, Bit errors = %d, BEP = %1.2e' %\
                (total_bit_count, total_bit_errors,\
                total_bit_errors/total_bit_count))
        Rate 1/3 Object
        kmax =  0, taumax = 0
        Bits Received = 9976, Bit errors = 251, BEP = 2.52e-02
        *****************************************************
        Bits Received = 9976, Bit errors = 251, BEP = 2.52e-02


        >>> # Compare a collection of simulation results with hard decision
        >>> # bounds
        >>> SNRdB = np.arange(0,12,.1)
        >>> Pb_uc = fec.conv_Pb_bound(1/3,7,[4, 12, 20, 72, 225],SNRdB,2)
        >>> Pb_s_third_3_hard = fec.conv_Pb_bound(1/3,8,[3, 0, 15, 0, 58, 0, 201, 0],SNRdB,0)
        >>> Pb_s_third_5_hard = fec.conv_Pb_bound(1/3,12,[12, 0, 12, 0, 56, 0, 320, 0],SNRdB,0)
        >>> Pb_s_third_7_hard = fec.conv_Pb_bound(1/3,14,[1, 0, 20, 0, 53, 0, 184],SNRdB,0)
        >>> Pb_s_third_5_hard_sim = np.array([8.94e-04,1.11e-04,8.73e-06])
        >>> plt.figure(figsize=(5,5))
        >>> plt.semilogy(SNRdB,Pb_uc)
        >>> plt.semilogy(SNRdB,Pb_s_third_3_hard,'r--')
        >>> plt.semilogy(SNRdB,Pb_s_third_5_hard,'g--')
        >>> plt.semilogy(SNRdB,Pb_s_third_7_hard,'k--')
        >>> plt.semilogy(np.array([5,6,7]),Pb_s_third_5_hard_sim,'sg')
        >>> plt.axis([0,12,1e-7,1e0])
        >>> plt.title(r'Hard Decision Rate 1/3 Coding Measurements')
        >>> plt.xlabel(r'$E_b/N_0$ (dB)')
        >>> plt.ylabel(r'Symbol Error Probability')
        >>> plt.legend(('Uncoded BPSK','R=1/3, K=3, Hard',\
                    'R=1/3, K=5, Hard', 'R=1/3, K=7, Hard',\
                    ),loc='upper right')
        >>> plt.grid();
        >>> plt.show()

        >>> # Show the traceback for the rate 1/3 hard decision case
        >>> cc2.traceback_plot()
        """
        if metric_type == 'hard':
            # If hard decision must have 0/1 integers for input else float
            if np.issubdtype(x.dtype, np.integer):
                if x.max() > 1 or x.min() < 0:
                    raise ValueError('Integer bit values must be 0 or 1')
            else:
                raise ValueError('Decoder inputs must be integers on [0,1] for hard decisions')
        # Initialize cumulative metrics array
        cm_present = np.zeros((self.Nstates,1))

        NS = len(x) # number of channel symbols to process; 
                     # must be even for rate 1/2
                     # must be a multiple of 3 for rate 1/3
        y = np.zeros(NS-self.decision_depth) # Decoded bit sequence
        k = 0
        symbolL = self.rate.denominator

        # Calculate branch metrics and update traceback states and traceback bits
        for n in range(0,NS,symbolL):
            cm_past = self.paths.cumulative_metric[:,0]
            tb_states_temp = self.paths.traceback_states[:,:-1].copy()
            tb_bits_temp = self.paths.traceback_bits[:,:-1].copy()
            for m in range(self.Nstates):
                d1 = self.bm_calc(self.branches.bits1[m],
                                    x[n:n+symbolL],metric_type,
                                    quant_level)
                d1 = d1 + cm_past[self.branches.states1[m]]
                d2 = self.bm_calc(self.branches.bits2[m],
                                    x[n:n+symbolL],metric_type,
                                    quant_level)
                d2 = d2 + cm_past[self.branches.states2[m]]
                if d1 <= d2: # Find the survivor assuming minimum distance wins
                    cm_present[m] = d1
                    self.paths.traceback_states[m,:] = np.hstack((self.branches.states1[m],
                                    tb_states_temp[int(self.branches.states1[m]),:]))
                    self.paths.traceback_bits[m,:] = np.hstack((self.branches.input1[m],
                                    tb_bits_temp[int(self.branches.states1[m]),:]))
                else:
                    cm_present[m] = d2
                    self.paths.traceback_states[m,:] = np.hstack((self.branches.states2[m],
                                    tb_states_temp[int(self.branches.states2[m]),:]))
                    self.paths.traceback_bits[m,:] = np.hstack((self.branches.input2[m],
                                    tb_bits_temp[int(self.branches.states2[m]),:]))
            # Update cumulative metric history
            self.paths.cumulative_metric = np.hstack((cm_present, 
                                            self.paths.cumulative_metric[:,:-1]))
            
            # Obtain estimate of input bit sequence from the oldest bit in 
            # the traceback having the smallest (most likely) cumulative metric
            min_metric = min(self.paths.cumulative_metric[:,0])
            min_idx = np.where(self.paths.cumulative_metric[:,0] == min_metric)
            if n >= symbolL*self.decision_depth-symbolL:  # 2 since Rate = 1/2
                y[k] = self.paths.traceback_bits[min_idx[0][0],-1]
                k += 1
        y = y[:k] # trim final length
        return y