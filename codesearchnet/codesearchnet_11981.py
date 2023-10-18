def _smartcast(castee, caster, subval=None):
    '''
    This just tries to apply the caster function to castee.

    Returns None on failure.

    '''

    try:
        return caster(castee)
    except Exception as e:
        if caster is float or caster is int:
            return nan
        elif caster is str:
            return ''
        else:
            return subval