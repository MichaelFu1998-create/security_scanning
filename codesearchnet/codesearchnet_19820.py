def listCount(l):
    """returns len() of each item in a list, as a list."""
    for i in range(len(l)):
        l[i]=len(l[i])
    return l