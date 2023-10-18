def filter_grompp_options(**kwargs):
    """Returns one dictionary only containing valid :program:`grompp` options and everything else.

    Option list is hard coded and nased on :class:`~gromacs.tools.grompp` 4.5.3.

    :Returns: ``(grompp_dict, other_dict)``

    .. versionadded:: 0.2.4
    """
    grompp_options = ('f','po','c','r','rb','n','p','pp','o','t','e',  # files
                      'h', 'noh', 'version', 'noversion', 'nice', 'v', 'nov',
                      'time', 'rmvsbds', 'normvsbds', 'maxwarn', 'zero', 'nozero',
                      'renum', 'norenum')
    grompp = dict((k,v) for k,v in kwargs.items() if k in grompp_options)
    other =  dict((k,v) for k,v in kwargs.items() if k not in grompp_options)
    return grompp, other