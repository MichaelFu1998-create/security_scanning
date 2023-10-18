def check_periodrec_alias(actualperiod,
                          recoveredperiod,
                          tolerance=1.0e-3):
    '''This determines what kind of aliasing (if any) exists between
    `recoveredperiod` and `actualperiod`.

    Parameters
    ----------

    actualperiod : float
        The actual period of the object.

    recoveredperiod : float
        The recovered period of the object.

    tolerance : float
        The absolute difference required between the input periods to mark the
        recovered period as close to the actual period.

    Returns
    -------

    str
        The type of alias determined for the input combination of periods. This
        will be CSV string with values taken from the following list, based on
        the types of alias found::

            ['actual',
             'twice',
             'half',
             'ratio_over_1plus',
             'ratio_over_1minus',
             'ratio_over_1plus_twice',
             'ratio_over_1minus_twice',
             'ratio_over_1plus_thrice',
             'ratio_over_1minus_thrice',
             'ratio_over_minus1',
             'ratio_over_twice_minus1']

    '''

    if not (np.isfinite(actualperiod) and np.isfinite(recoveredperiod)):

        LOGERROR("can't compare nan values for actual/recovered periods")
        return 'unknown'

    else:

        #################
        ## ALIAS TYPES ##
        #################

        # simple ratios
        twotimes_p = actualperiod*2.0
        half_p = actualperiod*0.5

        # first kind of alias
        alias_1a = actualperiod/(1.0+actualperiod)
        alias_1b = actualperiod/(1.0-actualperiod)

        # second kind of alias
        alias_2a = actualperiod/(1.0+2.0*actualperiod)
        alias_2b = actualperiod/(1.0-2.0*actualperiod)

        # third kind of alias
        alias_3a = actualperiod/(1.0+3.0*actualperiod)
        alias_3b = actualperiod/(1.0-3.0*actualperiod)

        # fourth kind of alias
        alias_4a = actualperiod/(actualperiod - 1.0)
        alias_4b = actualperiod/(2.0*actualperiod - 1.0)

        aliases = np.ravel(np.array([
            actualperiod,
            twotimes_p,
            half_p,
            alias_1a,
            alias_1b,
            alias_2a,
            alias_2b,
            alias_3a,
            alias_3b,
            alias_4a,
            alias_4b]
        ))
        alias_labels = np.array(ALIAS_TYPES)

        # check type of alias
        closest_alias = np.isclose(recoveredperiod, aliases, atol=tolerance)

        if np.any(closest_alias):

            closest_alias_type = alias_labels[closest_alias]
            return ','.join(closest_alias_type.tolist())

        else:

            return 'other'