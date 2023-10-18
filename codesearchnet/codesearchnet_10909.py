def sim_timetrace_bg2(emission, max_rate, bg_rate, t_step, rs=None):
    """Draw random emitted photons from r.v. ~ Poisson(emission_rates).

    This is an alternative implementation of :func:`sim_timetrace_bg`.
    """
    if rs is None:
        rs = np.random.RandomState()
    emiss_bin_rate = np.zeros((emission.shape[0] + 1, emission.shape[1]),
                              dtype='float64')
    emiss_bin_rate[:-1] = emission * max_rate * t_step
    if bg_rate is not None:
        emiss_bin_rate[-1] = bg_rate * t_step
        counts = rs.poisson(lam=emiss_bin_rate).astype('uint8')
    else:
        counts = rs.poisson(lam=emiss_bin_rate[:-1]).astype('uint8')
    return counts