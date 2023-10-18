def getOperationNameForId(i: int):
    """ Convert an operation id into the corresponding string
    """
    assert isinstance(i, (int)), "This method expects an integer argument"
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    raise ValueError("Unknown Operation ID %d" % i)