def normalize_cols(table):
    """
    Pad short rows to the length of the longest row to help render "jagged"
    CSV files
    """
    longest_row_len = max([len(row) for row in table])
    for row in table:
        while len(row) < longest_row_len:
            row.append('')
    return table