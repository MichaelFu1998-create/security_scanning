def originFormat(thing):
    """Try to format anything as a 2D matrix with column names."""
    if type(thing) is list and type(thing[0]) is dict:
        return originFormat_listOfDicts(thing)
    if type(thing) is list and type(thing[0]) is list:
        return originFormat_listOfDicts(dictFlat(thing))
    else:
        print(" !! I don't know how to format this object!")
        print(thing)