def window_visu(N=51, name='hamming', **kargs):
    """A Window visualisation tool

    :param N: length of the window
    :param name: name of the window
    :param NFFT: padding used by the FFT
    :param mindB: the minimum frequency power in dB
    :param maxdB: the maximum frequency power in dB
    :param kargs: optional arguments passed to :func:`create_window`

    This function plot the window shape and its equivalent in the Fourier domain.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'kaiser', beta=8.)

    """
    # get the default parameters
    mindB = kargs.pop('mindB', -100)
    maxdB = kargs.pop('maxdB', None)
    norm = kargs.pop('norm', True)

    # create a window object
    w = Window(N, name, **kargs)

    # plot the time and frequency windows
    w.plot_time_freq(mindB=mindB, maxdB=maxdB, norm=norm)