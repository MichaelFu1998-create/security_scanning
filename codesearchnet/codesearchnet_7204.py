def print_table(col_tuple, row_tuples):
    """Print column headers and rows as a reStructuredText table.

    Args:
        col_tuple: Tuple of column name strings.
        row_tuples: List of tuples containing row data.
    """
    col_widths = [max(len(str(row[col])) for row in [col_tuple] + row_tuples)
                  for col in range(len(col_tuple))]
    format_str = ' '.join('{{:<{}}}'.format(col_width)
                          for col_width in col_widths)
    header_border = ' '.join('=' * col_width for col_width in col_widths)
    print(header_border)
    print(format_str.format(*col_tuple))
    print(header_border)
    for row_tuple in row_tuples:
        print(format_str.format(*row_tuple))
    print(header_border)
    print()