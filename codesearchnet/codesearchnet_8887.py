def poisson_random_measure(t, rate, rate_max):
    """A function that returns the arrival time of the next arrival for
    a Poisson random measure.

    Parameters
    ----------
    t : float
        The start time from which to simulate the next arrival time.
    rate : function
        The *intensity function* for the measure, where ``rate(t)`` is
        the expected arrival rate at time ``t``.
    rate_max : float
        The maximum value of the ``rate`` function.

    Returns
    -------
    out : float
        The time of the next arrival.

    Notes
    -----
    This function returns the time of the next arrival, where the
    distribution of the number of arrivals between times :math:`t` and
    :math:`t+s` is Poisson with mean

    .. math::

       \int_{t}^{t+s} dx \, r(x)

    where :math:`r(t)` is the supplied ``rate`` function. This function
    can only simulate processes that have bounded intensity functions.
    See chapter 6 of [3]_ for more on the mathematics behind Poisson
    random measures; the book's publisher, Springer, has that chapter
    available online for free at (`pdf`_\).

    A Poisson random measure is sometimes called a non-homogeneous
    Poisson process. A Poisson process is a special type of Poisson
    random measure.

    .. _pdf: http://www.springer.com/cda/content/document/\
                cda_downloaddocument/9780387878584-c1.pdf

    Examples
    --------
    Suppose you wanted to model the arrival process as a Poisson
    random measure with rate function :math:`r(t) = 2 + \sin( 2\pi t)`.
    Then you could do so as follows:

    >>> import queueing_tool as qt
    >>> import numpy as np
    >>> np.random.seed(10)
    >>> rate  = lambda t: 2 + np.sin(2 * np.pi * t)
    >>> arr_f = lambda t: qt.poisson_random_measure(t, rate, 3)
    >>> arr_f(1)  # doctest: +ELLIPSIS
    1.491...

    References
    ----------
    .. [3] Cinlar, Erhan. *Probability and stochastics*. Graduate Texts in\
           Mathematics. Vol. 261. Springer, New York, 2011.\
           :doi:`10.1007/978-0-387-87859-1`
    """
    scale = 1.0 / rate_max
    t = t + exponential(scale)
    while rate_max * uniform() > rate(t):
        t = t + exponential(scale)
    return t