def subset(*args):
    """
    Pipeable subsetting method.

    Takes either
     - a dataframe and a tuple of arguments required for subsetting,
     - a tuple of arguments if a dataframe has already been piped into.

    :Example:
        
    subset(dataframe, "column")
    
    :Example:
    
    dataframe >> subset("column")

    :param args: tuple of arguments
    :type args: tuple
    :return: returns a dataframe object
    :rtype: DataFrame
    """

    if args and isinstance(args[0], dataframe.DataFrame):
        return args[0].subset(*args[1:])
    elif not args:
        raise ValueError("No arguments provided")
    else:
        return pipeable.Pipeable(pipeable.PipingMethod.SUBSET, *args)