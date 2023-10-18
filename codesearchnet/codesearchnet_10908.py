def sim_timetrace_bg(emission, max_rate, bg_rate, t_step, rs=None):
    """Draw random emitted photons from r.v. ~ Poisson(emission_rates).

    Arguments:
        emission (2D array): array of normalized emission rates. One row per
            particle (axis = 0). Columns are the different time steps.
        max_rate (float): the peak emission rate in Hz.
        bg_rate (float or None): rate of a constant Poisson background (Hz).
            Background is added as an additional row in the returned array
            of counts. If None, no background simulated.
        t_step (float): duration of a time step in seconds.
        rs (RandomState or None): object used to draw the random numbers.
            If None, a new RandomState is created using a random seed.

    Returns:
        `counts` an 2D uint8 array of counts in each time bin, for each
        particle. If `bg_rate` is None counts.shape == emission.shape.
        Otherwise, `counts` has one row more than `emission` for storing
        the constant Poisson background.
    """
    if rs is None:
        rs = np.random.RandomState()
    em = np.atleast_2d(emission).astype('float64', copy=False)
    counts_nrows = em.shape[0]
    if bg_rate is not None:
        counts_nrows += 1   # add a row for poisson background
    counts = np.zeros((counts_nrows, em.shape[1]), dtype='u1')
    # In-place computation
    # NOTE: the caller will see the modification
    em *= (max_rate * t_step)
    # Use automatic type conversion int64 (counts_par) -> uint8 (counts)
    counts_par = rs.poisson(lam=em)
    if bg_rate is None:
        counts[:] = counts_par
    else:
        counts[:-1] = counts_par
        counts[-1] = rs.poisson(lam=bg_rate * t_step, size=em.shape[1])
    return counts