def stereo_FM(x,fs=2.4e6,file_name='test.wav'):
    """
    Stereo demod from complex baseband at sampling rate fs.
    Assume fs is 2400 ksps
    
    Mark Wickert July 2017
    """
    N1 = 10
    b = signal.firwin(64,2*200e3/float(fs))
    # Filter and decimate (should be polyphase)
    y = signal.lfilter(b,1,x)
    z = ss.downsample(y,N1)
    # Apply complex baseband discriminator
    z_bb = discrim(z)
    # Work with the (3) stereo multiplex signals:
    # Begin by designing a lowpass filter for L+R and DSP demoded (L-R)
    # (fc = 12 KHz)
    b12 = signal.firwin(128,2*12e3/(float(fs)/N1))
    # The L + R term is at baseband, we just lowpass filter to remove 
    # other terms above 12 kHz.
    y_lpr = signal.lfilter(b12,1,z_bb)
    b19 = signal.firwin(128,2*1e3*np.array([19-5,19+5])/(float(fs)/N1),
                        pass_zero=False);
    z_bb19 = signal.lfilter(b19,1,z_bb)
    # Lock PLL to 19 kHz pilot
    # A type 2 loop with bandwidth Bn = 10 Hz and damping zeta = 0.707 
    # The VCO quiescent frequency is set to 19000 Hz.
    theta, phi_error = pilot_PLL(z_bb19,19000,fs/N1,2,10,0.707)
    # Coherently demodulate the L - R subcarrier at 38 kHz.
    # theta is the PLL output phase at 19 kHz, so to double multiply 
    # by 2 and wrap with cos() or sin().
    # First bandpass filter
    b38 = signal.firwin(128,2*1e3*np.array([38-5,38+5])/(float(fs)/N1),
                        pass_zero=False);
    x_lmr = signal.lfilter(b38,1,z_bb)
    # Coherently demodulate using the PLL output phase
    x_lmr = 2*np.sqrt(2)*np.cos(2*theta)*x_lmr
    # Lowpass at 12 kHz to recover the desired DSB demod term
    y_lmr = signal.lfilter(b12,1,x_lmr)
    # Matrix the y_lmr and y_lpr for form right and left channels:
    y_left = y_lpr + y_lmr
    y_right = y_lpr - y_lmr
    
    # Decimate by N2 (nominally 5)
    N2 = 5
    fs2 = float(fs)/(N1*N2) # (nominally 48 ksps)
    y_left_DN2 = ss.downsample(y_left,N2)
    y_right_DN2 = ss.downsample(y_right,N2)
    # Deemphasize with 75 us time constant to 'undo' the preemphasis 
    # applied at the transmitter in broadcast FM.
    # A 1-pole digital lowpass works well here.
    a_de = np.exp(-2.1*1e3*2*np.pi/fs2)
    z_left = signal.lfilter([1-a_de],[1, -a_de],y_left_DN2)
    z_right = signal.lfilter([1-a_de],[1, -a_de],y_right_DN2)
    # Place left and righ channels as side-by-side columns in a 2D array
    z_out = np.hstack((np.array([z_left]).T,(np.array([z_right]).T)))
    
    ss.to_wav(file_name, 48000, z_out/2)
    print('Done!')
    #return z_bb, z_out
    return z_bb, theta, y_lpr, y_lmr, z_out