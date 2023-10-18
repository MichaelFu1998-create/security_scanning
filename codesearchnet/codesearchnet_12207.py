def _fourier_func(fourierparams, phase, mags):
    '''This returns a summed Fourier cosine series.

    Parameters
    ----------

    fourierparams : list
        This MUST be a list of the following form like so::

            [period,
             epoch,
             [amplitude_1, amplitude_2, amplitude_3, ..., amplitude_X],
             [phase_1, phase_2, phase_3, ..., phase_X]]

        where X is the Fourier order.

    phase,mags : np.array
        The input phase and magnitude areas to use as the basis for the cosine
        series. The phases are used directly to generate the values of the
        function, while the mags array is used to generate the zeroth order
        amplitude coefficient.

    Returns
    -------

    np.array
        The Fourier cosine series function evaluated over `phase`.

    '''

    # figure out the order from the length of the Fourier param list
    order = int(len(fourierparams)/2)

    # get the amplitude and phase coefficients
    f_amp = fourierparams[:order]
    f_pha = fourierparams[order:]

    # calculate all the individual terms of the series
    f_orders = [f_amp[x]*npcos(2.0*pi_value*x*phase + f_pha[x])
                for x in range(order)]

    # this is the zeroth order coefficient - a constant equal to median mag
    total_f = npmedian(mags)

    # sum the series
    for fo in f_orders:
        total_f += fo

    return total_f