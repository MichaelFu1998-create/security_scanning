def get_ndx_groups(ndx, **kwargs):
    """Return a list of index groups in the index file *ndx*.

    :Arguments:
        - *ndx*  is a Gromacs index file.
        - kwargs are passed to :func:`make_ndx_captured`.

    :Returns:
        list of groups as supplied by :func:`parse_ndxlist`

    Alternatively, load the index file with
    :class:`gromacs.formats.NDX` for full control.
    """
    fd, tmp_ndx = tempfile.mkstemp(suffix='.ndx')
    kwargs['o'] = tmp_ndx
    try:
        g = parse_ndxlist(make_ndx_captured(n=ndx, **kwargs)[1])
    finally:
        utilities.unlink_gmx(tmp_ndx)
    return g