def aggregate(*args):
    """
    Pipeable aggregation method.
    
    Takes either 
     - a dataframe and a tuple of arguments required for aggregation,
     - a tuple of arguments if a dataframe has already been piped into.
    In any case one argument has to be a class that extends callable.

    :Example:

    aggregate(dataframe, Function, "new_col_name", "old_col_name")

    :Example:

    dataframe >> aggregate(Function, "new_col_name", "old_col_name")

    :param args: tuple of arguments
    :type args: tuple
    :return: returns a dataframe object
    :rtype: DataFrame
    """

    if args and isinstance(args[0], dataframe.DataFrame):
        return args[0].aggregate(args[1], args[2], *args[3:])
    elif not args:
        raise ValueError("No arguments provided")
    else:
        return pipeable.Pipeable(pipeable.PipingMethod.AGGREGATE, *args)