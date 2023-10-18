def dump(grids, mode=MODE_ZINC):
    """
    Dump the given grids in the specified over-the-wire format.
    """
    if isinstance(grids, Grid):
        return dump_grid(grids, mode=mode)
    _dump = functools.partial(dump_grid, mode=mode)
    if mode == MODE_ZINC:
        return '\n'.join(map(_dump, grids))
    elif mode == MODE_JSON:
        return '[%s]' % ','.join(map(_dump, grids))
    else: # pragma: no cover
        raise NotImplementedError('Format not implemented: %s' % mode)