def mono_FM(x,fs=2.4e6,file_name='test.wav'):
    """
    Decimate complex baseband input by 10
    Design 1st decimation lowpass filter (f_c = 200 KHz)
    """
    b = signal.firwin(64,2*200e3/float(fs))
    # Filter and decimate (should be polyphase)
    y = signal.lfilter(b,1,x)
    z = ss.downsample(y,10)
    # Apply complex baseband discriminator
    z_bb = discrim(z)
    # Design 2nd decimation lowpass filter (fc = 12 KHz)
    bb = signal.firwin(64,2*12e3/(float(fs)/10))
    # Filter and decimate
    zz_bb = signal.lfilter(bb,1,z_bb)
    # Decimate by 5
    z_out = ss.downsample(zz_bb,5)
    # Save to wave file
    ss.to_wav(file_name, 48000, z_out/2)
    print('Done!')
    return z_bb, z_out