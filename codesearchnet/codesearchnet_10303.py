def make_ndx_captured(**kwargs):
    """make_ndx that captures all output

    Standard :func:`~gromacs.make_ndx` command with the input and
    output pre-set in such a way that it can be conveniently used for
    :func:`parse_ndxlist`.

    Example::
      ndx_groups = parse_ndxlist(make_ndx_captured(n=ndx)[0])

    Note that the convenient :func:`get_ndx_groups` function does exactly
    that and can probably used in most cases.

    :Arguments:
        keywords are passed on to :func:`~gromacs.make_ndx`
    :Returns:
        (*returncode*, *output*, ``None``)
    """
    kwargs['stdout']=False   # required for proper output as described in doc
    user_input = kwargs.pop('input',[])
    user_input = [cmd for cmd in user_input if cmd != 'q']  # filter any quit
    kwargs['input'] = user_input + ['', 'q']                # necessary commands
    return gromacs.make_ndx(**kwargs)