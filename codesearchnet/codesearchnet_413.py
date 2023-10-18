def _stack_positions(positions, pos_in_dollars=True):
    """
    Convert positions to percentages if necessary, and change them
    to long format.

    Parameters
    ----------
    positions: pd.DataFrame
        Daily holdings (in dollars or percentages), indexed by date.
        Will be converted to percentages if positions are in dollars.
        Short positions show up as cash in the 'cash' column.

    pos_in_dollars : bool
        Flag indicating whether `positions` are in dollars or percentages
        If True, positions are in dollars.
    """
    if pos_in_dollars:
        # convert holdings to percentages
        positions = get_percent_alloc(positions)

    # remove cash after normalizing positions
    positions = positions.drop('cash', axis='columns')

    # convert positions to long format
    positions = positions.stack()
    positions.index = positions.index.set_names(['dt', 'ticker'])

    return positions