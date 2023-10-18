def IIR_bsf(f_pass1, f_stop1, f_stop2, f_pass2, Ripple_pass, Atten_stop, 
            fs = 1.00, ftype = 'butter'):
    """
    Design an IIR bandstop filter using scipy.signal.iirdesign. 
    The filter order is determined based on 
    f_pass Hz, f_stop Hz, and the desired stopband attenuation
    d_stop in dB, all relative to a sampling rate of fs Hz.

    Mark Wickert October 2016
    """
   
    b,a = signal.iirdesign([2*float(f_pass1)/fs, 2*float(f_pass2)/fs],
                           [2*float(f_stop1)/fs, 2*float(f_stop2)/fs],
                           Ripple_pass, Atten_stop,
                           ftype = ftype, output='ba')
    sos = signal.iirdesign([2*float(f_pass1)/fs, 2*float(f_pass2)/fs],
                           [2*float(f_stop1)/fs, 2*float(f_stop2)/fs],
                           Ripple_pass, Atten_stop,
                           ftype =ftype, output='sos')
    tag = 'IIR ' + ftype + ' order'
    print('%s = %d.' % (tag,len(a)-1))
    return b, a, sos