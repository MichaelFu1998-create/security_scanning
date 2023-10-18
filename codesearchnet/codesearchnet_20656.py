def _check_cols(df, col_names):
    """ Raise an AttributeError if `df` does not have a column named as an item of
    the list of strings `col_names`.
    """
    for col in col_names:
        if not hasattr(df, col):
            raise AttributeError("DataFrame does not have a '{}' column, got {}.".format(col,
                                                                                         df.columns))