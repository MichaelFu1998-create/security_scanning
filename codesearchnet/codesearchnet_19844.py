def findRelevantData(fileList,abfs):
    """return an abf of the *FIRST* of every type of thing."""
    relevant=[]
    things={}
    for abf in abfs:
        for fname in fileList:
            if abf in fname and not fname in relevant:
                relevant.append(fname)
    for item in sorted(relevant):
        thing = os.path.basename(item)
        if ".png" in thing:
            continue
        if not "_" in thing:
            continue
        thing=thing.split("_")[-1].split(".")[0]
        if not thing in things.keys(): #prevent overwriting
            things[thing]=item
    return things