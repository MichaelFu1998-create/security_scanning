def Positive(other_param, mode="invert", reroll_count_max=2):
    """
    Converts another parameter's results to positive values.

    Parameters
    ----------
    other_param : imgaug.parameters.StochasticParameter
        Other parameter which's sampled values are to be
        modified.

    mode : {'invert', 'reroll'}, optional
        How to change the signs. Valid values are ``invert`` and ``reroll``.
        ``invert`` means that wrong signs are simply flipped.
        ``reroll`` means that all samples with wrong signs are sampled again,
        optionally many times, until they randomly end up having the correct
        sign.

    reroll_count_max : int, optional
        If `mode` is set to ``reroll``, this determines how often values may
        be rerolled before giving up and simply flipping the sign (as in
        ``mode="invert"``). This shouldn't be set too high, as rerolling is
        expensive.

    Examples
    --------
    >>> param = Positive(Normal(0, 1), mode="reroll")

    Generates a normal distribution that has only positive values.

    """
    return ForceSign(
        other_param=other_param,
        positive=True,
        mode=mode,
        reroll_count_max=reroll_count_max
    )