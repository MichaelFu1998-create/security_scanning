def horiz_div(col_widths, horiz, vert, padding):
    """
    Create the column dividers for a table with given column widths.

    col_widths: list of column widths
    horiz: the character to use for a horizontal divider
    vert: the character to use for a vertical divider
    padding: amount of padding to add to each side of a column
    """
    horizs = [horiz * w for w in col_widths]
    div = ''.join([padding * horiz, vert, padding * horiz])
    return div.join(horizs)