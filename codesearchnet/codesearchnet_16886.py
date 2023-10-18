def parse(grid_str, mode=MODE_ZINC, charset='utf-8'):
    '''
    Parse the given Zinc text and return the equivalent data.
    '''
    # Decode incoming text (or python3 will whine!)
    if isinstance(grid_str, six.binary_type):
        grid_str = grid_str.decode(encoding=charset)

    # Split the separate grids up, the grammar definition has trouble splitting
    # them up normally.  This will truncate the newline off the end of the last
    # row.
    _parse = functools.partial(parse_grid, mode=mode,
            charset=charset)
    if mode == MODE_JSON:
        if isinstance(grid_str, six.string_types):
            grid_data = json.loads(grid_str)
        else:
            grid_data = grid_str
        if isinstance(grid_data, dict):
            return _parse(grid_data)
        else:
            return list(map(_parse, grid_data))
    else:
        return list(map(_parse, GRID_SEP.split(grid_str.rstrip())))