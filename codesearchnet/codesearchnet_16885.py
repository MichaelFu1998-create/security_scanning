def dump_grid(grid):
    """
    Dump a single grid to its ZINC representation.
    """
    header = 'ver:%s' % dump_str(str(grid._version), version=grid._version)
    if bool(grid.metadata):
        header += ' ' + dump_meta(grid.metadata, version=grid._version)
    columns = dump_columns(grid.column, version=grid._version)
    rows = dump_rows(grid)
    return '\n'.join([header, columns] + rows + [''])