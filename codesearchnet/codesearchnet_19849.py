def getParent2(abfFname,groups):
    """given an ABF and the groups dict, return the ID of its parent."""
    if ".abf" in abfFname:
        abfFname=os.path.basename(abfFname).replace(".abf","")
    for parentID in groups.keys():
        if abfFname in groups[parentID]:
            return parentID
    return abfFname