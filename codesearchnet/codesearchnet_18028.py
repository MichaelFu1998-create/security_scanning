def fit_comp(new_comp, old_comp, **kwargs):
    """
    Fits a new component to an old component

    Calls do_levmarq to match the .get() fields of the two objects. The
    parameters of new_comp are modified in place.

    Parameters
    ----------
    new_comp : :class:`peri.comps.comp`
        The new object, whose parameters to update to fit the field of
        `old_comp`. Must have a .get() attribute which returns an ndarray
    old_comp : peri.comp
        The old ilm to match to.

    Other Parameters
    ----------------
        Any keyword arguments to be passed to the optimizer LMGlobals
        through do_levmarq.

    See Also
    --------
    do_levmarq : Levenberg-Marquardt minimization using a random subset
        of the image pixels.
    """
    #resetting the category to ilm:
    new_cat = new_comp.category
    new_comp.category = 'ilm'
    fake_s = states.ImageState(Image(old_comp.get().copy()), [new_comp], pad=0,
            mdl=mdl.SmoothFieldModel())
    do_levmarq(fake_s, new_comp.params, **kwargs)
    new_comp.category = new_cat