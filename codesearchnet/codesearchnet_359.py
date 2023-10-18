def get_top_long_short_abs(positions, top=10):
    """
    Finds the top long, short, and absolute positions.

    Parameters
    ----------
    positions : pd.DataFrame
        The positions that the strategy takes over time.
    top : int, optional
        How many of each to find (default 10).

    Returns
    -------
    df_top_long : pd.DataFrame
        Top long positions.
    df_top_short : pd.DataFrame
        Top short positions.
    df_top_abs : pd.DataFrame
        Top absolute positions.
    """

    positions = positions.drop('cash', axis='columns')
    df_max = positions.max()
    df_min = positions.min()
    df_abs_max = positions.abs().max()
    df_top_long = df_max[df_max > 0].nlargest(top)
    df_top_short = df_min[df_min < 0].nsmallest(top)
    df_top_abs = df_abs_max.nlargest(top)
    return df_top_long, df_top_short, df_top_abs