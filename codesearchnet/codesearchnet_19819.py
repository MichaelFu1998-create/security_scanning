def dictFlat(l):
    """Given a list of list of dicts, return just the dicts."""
    if type(l) is dict:
        return [l]
    if "numpy" in str(type(l)):
        return l
    dicts=[]
    for item in l:
        if type(item)==dict:
            dicts.append(item)
        elif type(item)==list:
            for item2 in item:
                dicts.append(item2)
    return dicts