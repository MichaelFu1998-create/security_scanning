def md_table(table, *, padding=DEFAULT_PADDING, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.

    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    table = normalize_cols(table)
    table = pad_cells(table)
    header = table[0]
    body = table[1:]

    col_widths = [len(cell) for cell in header]
    horiz = horiz_div(col_widths, header_div, divider, padding)

    header = add_dividers(header, divider, padding)
    body = [add_dividers(row, divider, padding) for row in body]

    table = [header, horiz]
    table.extend(body)
    table = [row.rstrip() for row in table]
    return '\n'.join(table)