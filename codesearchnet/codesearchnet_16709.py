def read_range(filepath, range_expr, sheet=None, dict_generator=None):
    """Read values from an Excel range into a dictionary.

    `range_expr` ie either a range address string, such as "A1", "$C$3:$E$5",
    or a defined name string for a range, such as "NamedRange1".
    If a range address is provided, `sheet` argument must also be provided.
    If a named range is provided and `sheet` is not, book level defined name
    is searched. If `sheet` is also provided, sheet level defined name for the
    specified `sheet` is searched.
    If range_expr points to a single cell, its value is returned.

    `dictgenerator` is a generator function that yields keys and values of 
    the returned dictionary. the excel range, as a nested tuple of openpyxl's
    Cell objects, is passed to the generator function as its single argument.
    If not specified, default generator is used, which maps tuples of row and
    column indexes, both starting with 0, to their values.
    
    Args:
        filepath (str): Path to an Excel file.
        range_epxr (str): Range expression, such as "A1", "$G4:$K10", 
            or named range "NamedRange1"
        sheet (str): Sheet name (case ignored).
            None if book level defined range name is passed as `range_epxr`.
        dict_generator: A generator function taking a nested tuple of cells 
            as a single parameter.

    Returns:
        Nested list containing range values.
    """

    def default_generator(cells):
        for row_ind, row in enumerate(cells):
            for col_ind, cell in enumerate(row):
                yield (row_ind, col_ind), cell.value

    book = opxl.load_workbook(filepath, data_only=True)

    if _is_range_address(range_expr):
        sheet_names = [name.upper() for name in book.sheetnames]
        index = sheet_names.index(sheet.upper())
        cells = book.worksheets[index][range_expr]
    else:
        cells = _get_namedrange(book, range_expr, sheet)

    # In case of a single cell, return its value.
    if isinstance(cells, opxl.cell.Cell):
        return cells.value

    if dict_generator is None:
        dict_generator = default_generator

    gen = dict_generator(cells)
    return {keyval[0]: keyval[1] for keyval in gen}