def WelchPeriodogram(data, NFFT=None,  sampling=1., **kargs):
    r"""Simple periodogram wrapper of numpy.psd function.

    :param A: the input data
    :param int NFFT: total length of the final data sets (padded 
        with zero if needed; default is 4096)
    :param str window:

    :Technical documentation:

    When we calculate the periodogram of a set of data we get an estimation
    of the spectral density. In fact as we use a Fourier transform and a
    truncated segments the spectrum is the convolution of the data with a
    rectangular window which Fourier transform is

    .. math::

        W(s)= \frac{1}{N^2} \left[ \frac{\sin(\pi s)}{\sin(\pi s/N)} \right]^2

    Thus oscillations and sidelobes appears around the main frequency. One aim of t he tapering is to reduced this effects. We multiply data by a window whose  sidelobes are much smaller than the main lobe. Classical window is hanning window.  But other windows are available. However we must take into account this energy and divide the spectrum by energy of taper used. Thus periodogram becomes :

    .. math::

        D_k \equiv \sum_{j=0}^{N-1}c_jw_j \; e^{2\pi ijk/N}  \qquad k=0,...,N-1

    .. math::

        P(0)=P(f_0)=\frac{1}{2\pi W_{ss}}\arrowvert{D_0}\arrowvert^2

    .. math::

        P(f_k)=\frac{1}{2\pi W_{ss}} \left[\arrowvert{D_k}\arrowvert^2+\arrowvert{D_{N-k}}\arrowvert^2\right]        \qquad k=0,1,...,     \left( \frac{1}{2}-1 \right)

    .. math::

        P(f_c)=P(f_{N/2})= \frac{1}{2\pi W_{ss}} \arrowvert{D_{N/2}}\arrowvert^2

    with

    .. math::

        {W_{ss}} \equiv N\sum_{j=0}^{N-1}w_j^2


    .. plot::
        :width: 80%
        :include-source:

        from spectrum import WelchPeriodogram, marple_data
        psd = WelchPeriodogram(marple_data, 256)

    """
    from pylab import psd
    spectrum = Spectrum(data, sampling=1.)

    P = psd(data, NFFT, Fs=sampling, **kargs)
    spectrum.psd = P[0]
    #spectrum.__Spectrum_sides = 'twosided'

    return P, spectrum