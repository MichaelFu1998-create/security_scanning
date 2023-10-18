def read_xl(xl_path: str):
    """ Return the workbook from the Excel file in `xl_path`."""
    xl_path, choice = _check_xl_path(xl_path)
    reader = XL_READERS[choice]

    return reader(xl_path)