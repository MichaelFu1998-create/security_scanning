def create_window(N, name=None, **kargs):
    r"""Returns the N-point window given a valid name

    :param int N: window size
    :param str name: window name (default is *rectangular*). Valid names
        are stored in :func:`~spectrum.window.window_names`.
    :param kargs: optional arguments are:

        * *beta*: argument of the :func:`window_kaiser` function (default is 8.6)
        * *attenuation*: argument of the :func:`window_chebwin` function (default is 50dB)
        * *alpha*: argument of the
            1. :func:`window_gaussian` function (default is 2.5)
            2. :func:`window_blackman` function (default is 0.16)
            3. :func:`window_poisson` function (default is 2)
            4. :func:`window_cauchy` function (default is 3)
        * *mode*: argument :func:`window_flattop` function (default is *symmetric*, can be *periodic*)
        * *r*: argument of the :func:`window_tukey` function (default is 0.5).

    The following windows have been simply wrapped from existing librairies like
    NumPy:

        * **Rectangular**: :func:`window_rectangle`,
        * **Bartlett** or Triangular: see :func:`window_bartlett`,
        * **Hanning** or Hann: see :func:`window_hann`,
        * **Hamming**: see :func:`window_hamming`,
        * **Kaiser**: see :func:`window_kaiser`,
        * **chebwin**: see :func:`window_chebwin`.

    The following windows have been implemented from scratch:

        * **Blackman**: See :func:`window_blackman`
        * **Bartlett-Hann** : see :func:`window_bartlett_hann`
        * **cosine or sine**: see :func:`window_cosine`
        * **gaussian**: see :func:`window_gaussian`
        * **Bohman**: see :func:`window_bohman`
        * **Lanczos or sinc**: see :func:`window_lanczos`
        * **Blackman Harris**: see :func:`window_blackman_harris`
        * **Blackman Nuttall**: see :func:`window_blackman_nuttall`
        * **Nuttall**: see :func:`window_nuttall`
        * **Tukey**: see :func:`window_tukey`
        * **Parzen**: see :func:`window_parzen`
        * **Flattop**: see :func:`window_flattop`
        * **Riesz**: see :func:`window_riesz`
        * **Riemann**: see :func:`window_riemann`
        * **Poisson**: see :func:`window_poisson`
        * **Poisson-Hanning**: see :func:`window_poisson_hanning`

    .. todo:: on request taylor, potter, Bessel, expo,
        rife-vincent, Kaiser-Bessel derived (KBD)

    .. plot::
        :width: 80%
        :include-source:

        from pylab import plot, legend
        from spectrum import create_window

        data = create_window(51, 'hamming')
        plot(data, label='hamming')
        data = create_window(51, 'kaiser')
        plot(data, label='kaiser')
        legend()

    .. plot::
        :width: 80%
        :include-source:

        from pylab import plot, log10, linspace, fft, clip
        from spectrum import create_window, fftshift

        A = fft(create_window(51, 'hamming'), 2048) / 25.5
        mag = abs(fftshift(A))
        freq = linspace(-0.5,0.5,len(A))
        response = 20 * log10(mag)
        mindB = -60
        response = clip(response,mindB,100)
        plot(freq, response)

    .. seealso:: :func:`window_visu`, :func:`Window`, :mod:`spectrum.dpss`
    """
    if name is None:
        name = 'rectangle'
    name = name.lower()
    assert name in list(window_names.keys()), \
        """window name %s not implemented or incorrect. Try to use one of %s"""\
        % (name, window_names)


    # create the function name
    f = eval(window_names[name])

    windows_with_parameters = \
    {'kaiser': {'beta': eval(window_names['kaiser']).__defaults__[0]},
     'blackman': {'alpha': eval(window_names['blackman']).__defaults__[0]},
     'cauchy': {'alpha': eval(window_names['cauchy']).__defaults__[0]},
     'flattop': {'mode': eval(window_names['flattop']).__defaults__[0]},
     'gaussian': {'alpha': eval(window_names['gaussian']).__defaults__[0]},
     'chebwin': {'attenuation':eval(window_names['chebwin']).__defaults__[0]},
     'tukey': {'r':eval(window_names['tukey']).__defaults__[0]},
     'poisson': {'alpha': eval(window_names['poisson']).__defaults__[0]},
     'poisson_hanning': {'alpha':
                         eval(window_names['poisson_hanning']).__defaults__[0]},
     'taylor': {'nbar': eval(window_names['taylor']).__defaults__[0],
                'sll': eval(window_names['taylor']).__defaults__[0]},     
    }

    if name not in list(windows_with_parameters.keys()):
        if len(kargs) == 0:
            # no parameters, so we directly call the function
            w = f(N)
        else:
            raise ValueError("""
            Parameters do not match any of the window. The window provided
            do not expect any parameters. Try to remove the parameters""")
    elif name in list(windows_with_parameters.keys()):
        # user optional parameters are provided, scan them:
        dargs = {}
        for arg in list(kargs.keys()):
            # check that the parameters are valid, and obtain the default value
            try:
                default = windows_with_parameters[name][arg]
            except:
                raise ValueError("""
                    Invalid optional argument (%s) for %s window.
                    Valid optional arguments are (%s)""" % \
                    (arg, name, list(windows_with_parameters[name].keys())))
            # add the user parameter to the list of parameters
            dargs[arg] = kargs.get(arg, default)
        # call the proper function with the optional arguments
        w = f(N, **dargs)

    return w