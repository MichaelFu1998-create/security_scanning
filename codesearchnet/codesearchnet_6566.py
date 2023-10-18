def add_dividers(row, divider, padding):
    """Add dividers and padding to a row of cells and return a string."""
    div = ''.join([padding * ' ', divider, padding * ' '])
    return div.join(row)