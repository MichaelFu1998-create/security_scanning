def abfSort(IDs):
    """
    given a list of goofy ABF names, return it sorted intelligently.
    This places things like 16o01001 after 16901001.
    """
    IDs=list(IDs)
    monO=[]
    monN=[]
    monD=[]
    good=[]
    for ID in IDs:
        if ID is None:
            continue
        if 'o' in ID:
            monO.append(ID)
        elif 'n' in ID:
            monN.append(ID)
        elif 'd' in ID:
            monD.append(ID)
        else:
            good.append(ID)
    return sorted(good)+sorted(monO)+sorted(monN)+sorted(monD)