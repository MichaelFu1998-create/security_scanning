def get_sheet_list(xl_path: str) -> List:
    """Return a list with the name of the sheets in
    the Excel file in `xl_path`.
    """
    wb = read_xl(xl_path)

    if hasattr(wb, 'sheetnames'):
        return wb.sheetnames
    else:
        return wb.sheet_names()