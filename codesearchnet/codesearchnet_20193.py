def wrap(f_df, xref, size=1):
    """
    Memoizes an objective + gradient function, and splits it into
    two functions that return just the objective and gradient, respectively.

    Parameters
    ----------
    f_df : function
        Must be unary (takes a single argument)

    xref : list, dict, or array_like
        The form of the parameters

    size : int, optional
        Size of the cache (Default=1)
    """
    memoized_f_df = lrucache(lambda x: f_df(restruct(x, xref)), size)
    objective = compose(first, memoized_f_df)
    gradient = compose(destruct, second, memoized_f_df)
    return objective, gradient