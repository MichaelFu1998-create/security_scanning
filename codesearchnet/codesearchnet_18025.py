def do_levmarq_n_directions(s, directions, max_iter=2, run_length=2,
        damping=1e-3, collect_stats=False, marquardt_damping=True, **kwargs):
    """
    Optimization of a state along a specific set of directions in parameter
    space.

    Parameters
    ----------
        s : :class:`peri.states.State`
            The state to optimize
        directions : np.ndarray
            [n,d] element numpy.ndarray of the n directions in the d-
            dimensional space to optimize along. `directions` is trans-
            formed to a unit vector internally
    Other Parameters
    ----------------
        Any parameters passed to LMEngine.
    """
    # normal = direction / np.sqrt(np.dot(direction, direction))
    normals = np.array([d/np.sqrt(np.dot(d,d)) for d in directions])
    if np.isnan(normals).any():
        raise ValueError('`directions` must not be 0s or contain nan')
    obj = OptState(s, normals)
    lo = LMOptObj(obj, max_iter=max_iter, run_length=run_length, damping=
            damping, marquardt_damping=marquardt_damping, **kwargs)
    lo.do_run_1()
    if collect_stats:
        return lo.get_termination_stats()