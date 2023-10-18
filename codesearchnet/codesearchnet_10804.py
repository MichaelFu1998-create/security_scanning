def sccs_bit_sync(y,Ns):
    """
    rx_symb_d,clk,track = sccs_bit_sync(y,Ns)

    //////////////////////////////////////////////////////
     Symbol synchronization algorithm using SCCS
    //////////////////////////////////////////////////////
         y = baseband NRZ data waveform
        Ns = nominal number of samples per symbol
    
    Reworked from ECE 5675 Project
    Translated from m-code version
    Mark Wickert April 2014
    """
    # decimated symbol sequence for SEP
    rx_symb_d = np.zeros(int(np.fix(len(y)/Ns)))
    track = np.zeros(int(np.fix(len(y)/Ns)))
    bit_count = -1
    y_abs = np.zeros(len(y))
    clk = np.zeros(len(y))
    k = Ns+1 #initial 1-of-Ns symbol synch clock phase
    # Sample-by-sample processing required
    for i in range(len(y)):
        #y_abs(i) = abs(round(real(y(i))))
        if i >= Ns: # do not process first Ns samples
            # Collect timing decision unit (TDU) samples
            y_abs[i] = np.abs(np.sum(y[i-Ns+1:i+1]))
            # Update sampling instant and take a sample
            # For causality reason the early sample is 'i',
            # the on-time or prompt sample is 'i-1', and  
            # the late sample is 'i-2'.
            if (k == 0):
                # Load the samples into the 3x1 TDU register w_hat.
                # w_hat[1] = late, w_hat[2] = on-time; w_hat[3] = early.
                w_hat = y_abs[i-2:i+1]
                bit_count += 1
                if w_hat[1] != 0:
                    if w_hat[0] < w_hat[2]:
                        k = Ns-1
                        clk[i-2] = 1
                        rx_symb_d[bit_count] = y[i-2-int(np.round(Ns/2))-1]
                    elif w_hat[0] > w_hat[2]:
                        k = Ns+1
                        clk[i] = 1
                        rx_symb_d[bit_count] = y[i-int(np.round(Ns/2))-1]
                    else:
                        k = Ns
                        clk[i-1] = 1
                        rx_symb_d[bit_count] = y[i-1-int(np.round(Ns/2))-1]
                else:
                    k = Ns
                    clk[i-1] = 1
                    rx_symb_d[bit_count] = y[i-1-int(np.round(Ns/2))]
                track[bit_count] = np.mod(i,Ns)
        k -= 1
    # Trim the final output to bit_count
    rx_symb_d = rx_symb_d[:bit_count]
    return rx_symb_d, clk, track