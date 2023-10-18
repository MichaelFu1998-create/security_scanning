def group(*args):
    """
    Pipeable grouping method.

    Takes either
      - a dataframe and a tuple of strings for grouping,
      - a tuple of strings if a dataframe has already been piped into.
    
    :Example:
        
    group(dataframe, "column")
    
    :Example:
    
    dataframe >> group("column")
    
    :param args: tuple of arguments
    :type args: tuple
    :return: returns a grouped dataframe object
    :rtype: GroupedDataFrame
    """

    if args and isinstance(args[0], dataframe.DataFrame):
        return args[0].group(*args[1:])
    elif not args:
        raise ValueError("No arguments provided")
    else:
        return pipeable.Pipeable(pipeable.PipingMethod.GROUP, *args)