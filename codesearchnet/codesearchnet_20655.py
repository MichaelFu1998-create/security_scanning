def concat_sheets(xl_path: str, sheetnames=None, add_tab_names=False):
    """ Return a pandas DataFrame with the concat'ed
    content of the `sheetnames` from the Excel file in
    `xl_path`.

    Parameters
    ----------
    xl_path: str
        Path to the Excel file

    sheetnames: list of str
        List of existing sheet names of `xl_path`.
        If None, will use all sheets from `xl_path`.

    add_tab_names: bool
        If True will add a 'Tab' column which says from which
        tab the row comes from.

    Returns
    -------
    df: pandas.DataFrame
    """
    xl_path, choice = _check_xl_path(xl_path)

    if sheetnames is None:
        sheetnames = get_sheet_list(xl_path)

    sheets = pd.read_excel(xl_path, sheetname=sheetnames)

    if add_tab_names:
        for tab in sheets:
            sheets[tab]['Tab'] = [tab] * len(sheets[tab])

    return pd.concat([sheets[tab] for tab in sheets])