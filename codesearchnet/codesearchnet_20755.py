def modify(*args):
    """
    Pipeable modification method 
    
    Takes either 
     - a dataframe and a tuple of arguments required for modification,
     - a tuple of arguments if a dataframe has already been piped into.
    In any case one argument has to be a class that extends callable.

    :Example:

    modify(dataframe, Function, "new_col_name", "old_col_name")
    
    :Example:

    dataframe >> modify(Function, "new_col_name", "old_col_name")

    :param args: tuple of arguments
    :type args: tuple
    :return: returns a dataframe object
    :rtype: DataFrame
    """

    if args and isinstance(args[0], dataframe.DataFrame):
        return args[0].modify(args[1], args[2], *args[3:])
    elif not args:
        raise ValueError("No arguments provided")
    else:
        return pipeable.Pipeable(pipeable.PipingMethod.MODIFY, *args)