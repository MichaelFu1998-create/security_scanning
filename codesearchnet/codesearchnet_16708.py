def _get_range(book, range_, sheet):
    """Return a range as nested dict of openpyxl cells."""

    filename = None
    if isinstance(book, str):
        filename = book
        book = opxl.load_workbook(book, data_only=True)
    elif isinstance(book, opxl.Workbook):
        pass
    else:
        raise TypeError

    if _is_range_address(range_):
        sheet_names = [name.upper() for name in book.sheetnames]
        index = sheet_names.index(sheet.upper())
        data = book.worksheets[index][range_]
    else:
        data = _get_namedrange(book, range_, sheet)
        if data is None:
            raise ValueError(
                "Named range '%s' not found in %s" % (range_, filename or book)
            )

    return data