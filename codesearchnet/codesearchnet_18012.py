def name_globals(s, remove_params=None):
    """
    Returns a list of the global parameter names.

    Parameters
    ----------
        s : :class:`peri.states.ImageState`
            The state to name the globals of.
        remove_params : Set or None
            A set of unique additional parameters to remove from the globals
            list.

    Returns
    -------
        all_params : list
            The list of the global parameter names, with each of
            remove_params removed.
    """
    all_params = s.params
    for p in s.param_particle(np.arange(s.obj_get_positions().shape[0])):
        all_params.remove(p)
    if remove_params is not None:
        for p in set(remove_params):
            all_params.remove(p)
    return all_params