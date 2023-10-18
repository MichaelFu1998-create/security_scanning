def duplicated(values: Sequence):
    """ Return the duplicated items in `values`"""
    vals = pd.Series(values)
    return vals[vals.duplicated()]