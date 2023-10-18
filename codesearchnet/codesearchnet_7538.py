def chirp(t, f0=0., t1=1., f1=100., form='linear', phase=0):
    r"""Evaluate a chirp signal at time t.

    A chirp signal is a frequency swept cosine wave.

    .. math:: a = \pi  (f_1 - f_0) / t_1
    .. math:: b = 2  \pi  f_0
    .. math:: y = \cos\left( \pi\frac{f_1-f_0}{t_1}  t^2 + 2\pi f_0 t + \rm{phase} \right)

    :param array t: times at which to evaluate the chirp signal
    :param float f0: frequency at time t=0 (Hz)
    :param float t1: time t1
    :param float f1: frequency at time t=t1 (Hz)
    :param str form: shape of frequency sweep in ['linear', 'quadratic', 'logarithmic']
    :param float phase: phase shift at t=0

    The parameter **form** can be:

        * 'linear'      :math:`f(t) = (f_1-f_0)(t/t_1) + f_0`
        * 'quadratic'   :math:`f(t) = (f_1-f_0)(t/t_1)^2 + f_0`
        * 'logarithmic' :math:`f(t) = (f_1-f_0)^{(t/t_1)} + f_0`

    Example:

    .. plot::
        :include-source:
        :width: 80%

        from spectrum import chirp
        from pylab import linspace, plot
        t = linspace(0, 1, 1000)
        y = chirp(t, form='linear')
        plot(y)
        y = chirp(t, form='quadratic')
        plot(y, 'r')

    """
    valid_forms = ['linear', 'quadratic', 'logarithmic']
    if form not in valid_forms:
        raise ValueError("Invalid form. Valid form are %s"
            % valid_forms)
    t = numpy.array(t)
    phase = 2. * pi * phase / 360.
    if form == "linear":
        a = pi * (f1 - f0)/t1
        b = 2. * pi * f0
        y = numpy.cos(a * t**2 + b*t + phase)
    elif form == "quadratic":
        a = (2/3. * pi * (f1-f0)/t1/t1)
        b = 2. * pi * f0
        y = numpy.cos(a*t**3 + b * t + phase)
    elif form == "logarithmic":
        a = 2. * pi * t1/numpy.log(f1-f0)
        b = 2. * pi * f0
        x = (f1-f0)**(1./t1)
        y = numpy.cos(a * x**t + b * t + phase)

    return y